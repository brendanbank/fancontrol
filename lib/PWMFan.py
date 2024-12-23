from machine import Pin, I2C
import time
from EMC2101 import EMC2101
import logging

_PIN_I2C0_SDA = Pin(6)
_PIN_I2C0_SCL = Pin(7)
_I2C0_FREQ = 400_000


import logging
log = logging.getLogger(__name__)


def normalize (current_temperature,
               delta = 4,
               target_temperature = 21.5,
               fan_min = 0,
               fan_max = 100,
               ):
    
    if delta == 0:
        log.critical( 'delta temperature = 0 setting it to 1')
        delta = 1
        
    _target_temperature  = target_temperature - (target_temperature*0.02)
    
    fanspeed = (current_temperature - _target_temperature) / delta * 100    
    fanspeed = max(min(fan_max, fanspeed),fan_min)
    if fanspeed > 0 and fanspeed < 10:
        fanspeed = 10
    return (fanspeed)

class PWMFan():
    def __init__(self,
                 i2c,
                 timeout = 5000):
        self.timeout = timeout
        self.fan_controller = EMC2101(i2c)
        self._percentage = 0
        self._last_changed = time.ticks_ms()
        self.percentage = 100

    @property
    def percentage(self):
        return(round(self._percentage,2))
    
    @property
    def rpm(self):
        return(self.fan_controller.get_fan_rpm())
    
    @percentage.setter
    def percentage(self, percentage):
        
        if self._percentage == percentage:
            return

        
        if time.ticks_diff(time.ticks_ms(), self._last_changed) < self.timeout and self._percentage > percentage:
            log.warning(f'timeout of {self.timeout} ticks not reached: {time.ticks_diff(time.ticks_ms(), self._last_changed)} ticks')
            return
        
        
        
        self._last_changed = time.ticks_ms()
        
        self._percentage=percentage
        self.fan_controller.set_duty_cycle(int(percentage))


if __name__ == '__main__':
    _PIN_I2C0_SDA = Pin(6)
    _PIN_I2C0_SCL = Pin(7)
    _I2C0_FREQ = 400_000
    i2c = I2C(0, scl=_PIN_I2C0_SCL, sda=_PIN_I2C0_SDA, freq=_I2C0_FREQ)

    fan=PWMFan(i2c, timeout=0)
    print (fan.percentage)
    fan.percentage = 0
    print (fan.percentage)
