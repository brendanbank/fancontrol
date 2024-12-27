import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import os
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

from configuration import Configuration

if __name__ == "__main__":
    
    log.debug("started")
    BASE = dict()
    config = Configuration(BASE, configfile="/Users/brendan/src/fancontrol/config.json")
    config.config_to_factory('fancontrol/config_items')
    
    config_item = config.get_config_item('wifi')
    
    print (config_item.item_name)
    
#     
#     config_vars = wifi.configuration
#     print (config_vars.ssid)
#     print (config.wifi.ssid)
# 