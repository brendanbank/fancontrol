import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import logging
log = logging.getLogger(__name__)
import re

from fancontrol.config import config
from configuration import BaseItem
from uforms import BaseForm, TextField, NumberField, CheckboxField, PasswordField, DisableCheckboxField, LayoutHR
from uforms.validators import validate_hostname
from microdot.utemplate import Template


def validate_hostname(hostname):
    ValidHostnameRegex = "^[\w\.-]+$"
    regex = re.compile(ValidHostnameRegex)
    log.debug(f'validate {hostname}: {regex.search(hostname)}')
    return True if regex.search(hostname) else False


class MQTTForm(BaseForm):
    form_description = 'MQTT Configuration'
    
    enable = DisableCheckboxField(label="Enable MQTT", value="on", required=False)
    hr_line_1 = LayoutHR(value="Broker Configuration")
    broker_hostname = TextField(label="Broker Hostname", css="col-md-6", error_txt="can only contain numbers and letters.", validation=validate_hostname)
    broker_port = NumberField(label="Broker Port", value=1883, css="col-md-6", error_txt="can only contain numbers")
    broker_username = TextField(label="Broker Username", css="col-md-6")
    broker_password = PasswordField(label="Broker Password", css="col-md-6", show_password=True)
    broker_ssl = CheckboxField(label="Use Secure Socket Layer (SSL)?", value="on", required=False)
    hr_line_2 = LayoutHR(value="Channel Configuration")
    logging_channel = TextField(label="Logging channel", value="fancontrol/logging", css="col-md-4")
    reporting_channel = TextField(label="Reporting channel", value="fancontrol/reporting", css="col-md-4")
    command_channel = TextField(label="Command channel", value="fancontrol/command", css="col-md-4")
    hr_line_3 = LayoutHR()    

class MQTTConfiguration(BaseItem):
    _priority = 2
    
    """ MQTT Configuration class """
    config_attribute = True
    item_name = 'mqtt'
    
    def __init__(self, application_configuration, item_configuration):
        log.debug(f'{self.__class__.__name__} started')
        
        super().__init__(application_configuration, item_configuration)
        self.formcls = MQTTForm
        self.form_description = self.formcls.form_description

        
