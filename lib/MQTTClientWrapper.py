import asyncio
from umqtt.robust import MQTTClient
import ubinascii
import machine
import time

class MQTTClientWrapper:
    def __init__(self, client_id, broker, port=1883, user=None, password=None):
        """Initialize the MQTT client with necessary details."""
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.client = None

    async def connect(self):
        """Connect to the MQTT broker asynchronously."""
        self.client = MQTTClient(self.client_id, self.broker, port=self.port, user=self.user, password=self.password)
        print(f"Connecting to MQTT broker {self.broker}...")
        try:
            self.client.connect()
            print("Connected to MQTT broker.")
        except Exception as e:
            print(f"Failed to connect: {e}")

    async def disconnect(self):
        """Disconnect from the MQTT broker asynchronously."""
        if self.client:
            self.client.disconnect()
            print("Disconnected from MQTT broker.")

    async def publish(self, topic, message):
        """Publish a message to a topic asynchronously."""
        if self.client:
            print(f"Publishing to {topic}: {message}")
            self.client.publish(topic, message)

    async def subscribe(self, topic, callback):
        """Subscribe to a topic with a callback for incoming messages."""
        if self.client:
            print(f"Subscribing to {topic}...")
            self.client.set_callback(callback)
            self.client.subscribe(topic)

    async def listen(self):
        """Listen for incoming messages on subscribed topics."""
        if self.client:
            print("Listening for messages...")
            try:
                while True:
                    self.client.check_msg()  # This checks for incoming messages
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                print("Stopped listening.")
                await self.disconnect()

    def handle_message(self, topic, msg):
        """Handle incoming messages from the subscribed topics."""
        print(f"Received message: {msg} on topic: {topic}")

    async def reconnect(self):
        """Reconnect to the broker if the connection is lost."""
        try:
            await self.connect()
            print("Reconnected to MQTT broker.")
        except Exception as e:
            print(f"Reconnect failed: {e}")


# Example of usage:


