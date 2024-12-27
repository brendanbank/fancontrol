import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
from configuration import ItemBase

class MQTTConfiguration(ItemBase):
    _priority = 2
    
    """ wifi configuration class """
    config_attribute = True
    config_name = 'mqtt'
    config_description = 'MQTT Configuration'
