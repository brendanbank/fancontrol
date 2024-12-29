import sys
# sys.path.append('/Users/brendan/src/fancontrol/lib')
from configuration import ItemBase
import logging
log = logging.getLogger(__name__)

actions = {
    "config_ap": {
        "settings": {
            "ap_ssid": "text",
            "ap_password": "password",
            },
        }
    
    }

class WiFiConfiguration(ItemBase):
    """ wifi configuration class """
    _priority = 1    
    item_name = 'wifi'
    item_description = 'WiFi Configuration'
    
    def __init__(self, application_configuration, item_configuration):
        log.debug(f'WiFiConfiguration started')
        super().__init__(application_configuration, item_configuration)
        self.config_ap()
            
    def config_ap(self):
        if not self.item_configuration.ap_ssid:
            self.item_configuration.ap_ssid = self.application_configuration.hostname
        if not self.item_configuration.ap_password:
            self.item_configuration.ap_password = "password"

        
        
            