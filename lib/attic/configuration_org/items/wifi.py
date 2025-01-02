import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
from uconfiguration import ItemBase
import logging
log = logging.getLogger(__name__)


class WiFiConfiguration(ItemBase):
    _priority = 1
    
    """ wifi uconfiguration class """    """ wifi uconfiguration class """
    config_attribute = True
    config_name = 'wifi'
    config_description = 'WiFi Configuration'
    config_vars = ['ssid', 'password', 'ap_ssid', 'ap_password']
    
    def __init__(self, application_configuration, item_configuration):
        log.debug(f'WiFiConfiguration started')
        super().__init__(application_configuration, item_configuration)
        
        if not item_configuration.ap_ssid:
            item_configuration.ap_ssid = application_configuration.application_name
        if not item_configuration.ap_password:
            item_configuration.ap_password = "password"
            