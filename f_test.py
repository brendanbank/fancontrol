import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import os
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


from configuration import Configuration

if __name__ == "__main__":
    
    log.debug("started")
    DICT_OBJ = dict ()
    config = Configuration(DICT_OBJ, configfile="/Users/brendan/src/fancontrol/config.json")
#     
# #     config.namespace("myhope")
# #     config.myhope.now = 1
#     
#     wifi = config.get_config_item('wifi')
#     
#     config_vars = wifi.configuration
#     print (config_vars.ssid)
#     print (config.wifi.ssid)
# 