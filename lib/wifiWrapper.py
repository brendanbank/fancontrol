import network
import socket
import time
import os
import ubinascii
import machine
import logging

log = logging.getLogger(__name__)

class WiFiManager:
    def __init__(self, credentials_file="wifi_config.txt", machine_id = ubinascii.hexlify(machine.unique_id()).decode()):
        self.credentials_file = credentials_file
        self.machine_id = machine_id
        self.wlan = network.WLAN(network.STA_IF)  # Station mode
        self.ap = network.WLAN(network.AP_IF)     # Access Point mode

    def load_credentials(self):
        """Load saved Wi-Fi credentials from the file."""
        try:
            with open(self.credentials_file, "r") as f:
                ssid = f.readline().strip()
                password = f.readline().strip()
                password = url_decode(password)
                password = password.encode('latin1').decode('utf-8')  # Decode UTF-8 password
                print(f"Loaded credentials: SSID={ssid}")
                return ssid, password
        except OSError as e:
            log.warning(f'No saved credentials file found.')
            return None, None

    def save_credentials(self, ssid, password):
        """Save Wi-Fi credentials to the file."""
        password = url_decode(password)
        password = password.encode('utf-8').decode('latin1')  # Encode as UTF-8
        with open(self.credentials_file, "w") as f:
            f.write(f"{ssid}\n")
            f.write(f"{password}\n")
        print("Credentials saved.")


    def ip(self):
        return (self.wlan.ifconfig()[0])
            
    def start_ap(self, essid=None, authmode=0):
        """Start the access point."""
        if not essid:
            essid = "PicoLan_" + str(self.machine_id)
        self.ap.active(True)
        self.ap.config(essid=essid, security=authmode)  # WPA2 by default
        log.warning(f"Access Point started. Connect to '{essid}'.")

    def stop_ap(self):
        """Stop the access point."""
        self.ap.active(False)
        print("Access Point stopped.")

    def connect_to_wifi(self, ssid, password):
        """Connect to a Wi-Fi network."""
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        print(f"Connecting to Wi-Fi network '{ssid}'... {password}")
        for _ in range(15):  # Wait up to 15 seconds
            if self.wlan.isconnected():
                print("Connected to Wi-Fi!")
                print("IP Address:", self.wlan.ifconfig()[0])
                return True
            time.sleep(1)
        print("Failed to connect to Wi-Fi.")
        self.wlan.active(False)
        return False

    def scan_networks(self):
        """Scan for available Wi-Fi networks."""
        self.wlan.active(True)
        networks = self.wlan.scan()  # Returns a list of tuples
        ssid_list = []
        for network in networks:
            ssid = network[0].decode('utf-8')  # Decode SSID
            if ssid not in ssid_list:         # Avoid duplicates
                ssid_list.append(ssid)
        return ssid_list

    def web_server(self):
        self.start_ap()
        """Start a simple web server for Wi-Fi uconfiguration."""
        addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        s.settimeout(300)
        print("Web server running on http://192.168.4.1")

        while True:
            try:
                cl, addr = s.accept()
            except KeyboardInterrupt:
                s.close()
                self.stop_ap()
                raise
            except OSError as e:
                if e.errno == 110:
                    print ("Socket Timeout, try to connect again to save credentials (if they are there).")
                    self.stop_ap()
                    s.close()
                    return (False)
                else:
                    s.close()
                    raise  # Re-raise the exception if it's not ETIMEOUT
            
            print("Client connected from", addr)
            request = cl.recv(1024)
            request = str(request)

            # Parse SSID and password from request
            ssid_start = request.find("ssid=")
            password_start = request.find("password=")
            if ssid_start != -1 and password_start != -1:
                ssid = request[ssid_start + 5:request.find("&", ssid_start)]
                password = request[password_start + 9:request.find(" ", password_start)]
                ssid = ssid.replace("+", " ").replace("%20", " ")
                password = url_decode(password)
                password = password.replace("+", " ").replace("%20", " ")
                print(f"Received SSID: {ssid}, Password: {password}")

                # Save credentials and attempt to connect
                self.save_credentials(ssid, password)
                cl.send("HTTP/1.1 200 OK\n\n")
                cl.send("Connecting to Wi-Fi. Please wait...")
                cl.close()
#                 self.stop_ap()
                if self.connect_to_wifi(ssid, password):
                    break
                else:
                    s.close()
                    return (False)

            # Perform Wi-Fi scan
            networks = self.scan_networks()
            options = "".join([f"<option value='{ssid}'>{ssid}</option>" for ssid in networks])

            # Serve a uconfiguration form
            html = f"""<!DOCTYPE html>
            <html>
            <head><title>Wi-Fi Configuration</title></head>
            <body>
                <h1>Configure Wi-Fi</h1>
                <form action="/" method="GET">
                    <label>SSID:</label>
                    <select name="ssid">
                        <option value="" disabled selected>Select a network</option>
                        {options}
                    </select><br><br>
                    <label>Password:</label>
                    <input type="password" name="password"><br><br>
                    <button type="submit">Connect</button>
                </form>
            </body>
            </html>
            """
            cl.send("HTTP/1.1 200 OK\n\n" + html)
            cl.close()
        s.close()
        return (True)

    def start(self):
        """Main entry point to handle Wi-Fi uconfiguration."""
        ssid, password = self.load_credentials()
    
        if ssid and password:
            # Try to connect with saved credentials
            
            if not self.connect_to_wifi(ssid, password):
                print("Failed to connect with saved credentials. Starting AP mode.")
                while not self.web_server():
                    pass
        else:
            # No saved credentials, start AP mode
            while not self.web_server():
                pass
            
def url_decode(encoded_str):
    """Decodes a URL-encoded string."""
    result = ""
    i = 0
    while i < len(encoded_str):
        char = encoded_str[i]
        if char == "%":
            # Decode the next two characters as a hex value
            hex_value = encoded_str[i+1:i+3]
            result += chr(int(hex_value, 16))
            i += 3
        elif char == "+":
            # Replace '+' with a space
            result += " "
            i += 1
        else:
            # Keep the character as is
            result += char
            i += 1
    return result


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    wifi = WiFiManager()
    wifi.start()

