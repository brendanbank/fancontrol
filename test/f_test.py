import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import os
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

from configuration import Configuration, ItemFactory

if __name__ == "__main__":
    
    log.debug("started")
    config = Configuration(configfile="config.json")
    factory = ItemFactory('test', config)
    
    print (config.factory._list)
    
    config.test = "test"
        
#     config_item = config.get_config_item('wifi')
#     
#     print (config_item.item_name)
    
#     
#     config_vars = wifi.configuration
#     print (config_vars.ssid)
#     print (config.wifi.ssid)
# 