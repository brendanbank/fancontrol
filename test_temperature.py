from machine import Pin, I2C, unique_id
import time
from EMC2101 import EMC2101
from sht45 import Sht45
from PWMFan import PWMFan, normalize
import asyncio
import ubinascii
import ulog as logging


log = logging.getLogger(__name__)

async def fancontrol():
    
    while True:

        fan.percentage = normalize(measurement.temperature)
        log.info (f'temperature = {measurement.temperature}°C humidity = {measurement.humidity}% fan percentage = {fan.percentage}% rpm = {fan.rpm}')
        
        await asyncio.sleep(1)

async def free_memory():
    while True:
        print (f'Memory {free()}')
        await asyncio.sleep(10)
    
def free(full=True):
  gc.collect()
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))


async def main():

    tasks = []
    tasks.append(asyncio.create_task (fancontrol()))
    tasks.append(asyncio.create_task (free_memory()))
    
    
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    _PIN_I2C0_SDA = Pin(6)
    _PIN_I2C0_SCL = Pin(7)
    _I2C0_FREQ = 400_000
    
    i2c = I2C(0, scl=_PIN_I2C0_SCL, sda=_PIN_I2C0_SDA, freq=_I2C0_FREQ)

    measurement = Sht45(i2c, cache_timeout=0)
    fan = PWMFan(i2c)
    
    MACHINE_ID = ubinascii.hexlify(unique_id())
    MQTT_SERVER = "srv6.bgwlan.nl"
    TOPIC = b'enviroment'


    try:
        os.remove ("config.json")
    except:
        pass
    
    config = {
        'target_temperature': 20.5 ,
        'after_run_time': 60,
        'min_fan': 15,
        'max_fan': 100}
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        fan.percentage = 100
        pass
    except Exception as e:
        print (f"Something went wrong: {e}")
        raise

    