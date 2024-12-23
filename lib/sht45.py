
from machine import I2C, Pin
import time
import logging

# SHT45 I2C address
SHT45_ADDRESS = 0x44

# Commands
CMD_MEASURE_HIGH = b'\xFD'

class Sht45():
    def __init__(self,i2c,cache_timeout=5):
        self.raw = None
        self.last_time = time.time()
        self.cache_timeout = cache_timeout
        self.i2c = i2c
        self.read_data()
        
    @property
    def temperature(self):
        return (self.convert_temperature())

    @property
    def humidity(self):
        return (self.convert_humidity())
    
    def check_cache(self):
#         print (f'time {self.last_time + self.cache_timeout} < {time.time()}')
        if (self.last_time + self.cache_timeout) < time.time():
            self.read_data()

    def read_data(self):
        if (self.cache_timeout > 2):
            logging.debug ("fetched raw data from sht45")
        self.i2c.writeto(SHT45_ADDRESS, CMD_MEASURE_HIGH)
        time.sleep(0.01)  # Wait for measurement
        self.last_time = time.time()
        self.raw = self.i2c.readfrom(SHT45_ADDRESS, 6)  # Read 6 bytes

    def convert_temperature(self):
        self.check_cache()            
        temp_raw = self.raw[0] << 8 | self.raw[1]
        temperature = -45 + (175 * (temp_raw / 65535))
        return round(temperature,2)

    def convert_humidity(self):
        self.check_cache()
        hum_raw = self.raw[3] << 8 | self.raw[4]
        humidity = 100 * (hum_raw / 65535)
        return round(humidity,2)

if __name__ == '__main__':
    _PIN_I2C0_SDA = Pin(6)
    _PIN_I2C0_SCL = Pin(7)
    _I2C0_FREQ = 400_000
    
    i2c = I2C(0, scl=_PIN_I2C0_SCL, sda=_PIN_I2C0_SDA, freq=_I2C0_FREQ)
    sht45 = Sht45(i2c)
    for i in range (1,10):
        print (f'temp: {sht45.temperature:.2f} humidity: {sht45.humidity:.2f}')
        time.sleep (1)
    
    