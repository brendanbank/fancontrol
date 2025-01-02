import sys
sys.path.append('/Users/brendan/src/fancontrol/configuration_test')

from items import BaseItem

import logging
log = logging.getLogger(__name__)

class WiFiConfiguration(BaseItem):
    """ wifi uconfiguration class """
    _priority = 1    
    item_name = 'wifi'
    config_description = 'WiFi Configuration'
    startup_actions = [ 'config_ap' ]
    
    def __init__(self, application_configuration, item_configuration):
        log.debug(f'WiFiConfiguration started')
        super().__init__(application_configuration, item_configuration)
        
        item_configuration.test = 0
    
    def config_ap(self):
        if not self.item_configuration.ap_ssid:
            self.item_configuration.ap_ssid = self.application_configuration.hostname
        if not self.item_configuration.ap_password:
            self.item_configuration.ap_password = "password"

