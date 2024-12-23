import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
from configuration.factory import BaseConfiguration

class MQTTConfiguration(BaseConfiguration):
    """ wifi configuration class """
    config_attribute = True
    config_name = 'mqtt'
    config_description = 'MQTT Configuration'
