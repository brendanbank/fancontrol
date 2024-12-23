import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
from configuration.factory import BaseConfiguration

class WiFiConfiguration(BaseConfiguration):
    """ wifi configuration class """
    config_attribute = True
    config_name = 'wifi'
    config_description = 'WiFi Configuration'
    
    config_vars = ['ssid', 'password', 'hostname']
    