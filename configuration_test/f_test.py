import sys
sys.path.append('/Users/brendan/src/fancontrol')
sys.path.append('/Users/brendan/src/fancontrol/lib')
sys.path.append('/Users/brendan/src/fancontrol/configuration_test')
import os
import logging
from uconfiguration.storage.json import JsonStorage

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

from uconfiguration.uconfiguration import Configuration
from items import ItemFactory

if __name__ == "__main__":
    
    log.debug("started")
    storage = JsonStorage(configfile="config.json")    
    config = Configuration(storage)
#     config.load_config()
    factory = ItemFactory('test', config)
    
    print (factory)
    
    config.test = "test"
    
    print(config)
        
#     config_item = config.get_config_item('wifi')
#     
#     print (config_item.item_name)
    
#     
#     config_vars = wifi.uconfiguration
#     print (config_vars.ssid)
#     print (config.wifi.ssid)
# 