import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import logging
log = logging.getLogger(__name__)
import re

from fancontrol.config import config
from configuration import ItemBase
from mforms import BaseForm, TextField, NumberField, CheckboxField, PasswordField, LayoutHR
from mforms.validators import validate_hostname
from microdot.utemplate import Template

def validate_hostname(hostname):
    ValidHostnameRegex="^[\w\.-]+$"
    regex = re.compile(ValidHostnameRegex)
    log.debug(f'validate {hostname}: {regex.search(hostname)}')
    return True if regex.search(hostname) else False

class MQTTForm(BaseForm):
    hr_line_1 = LayoutHR(value="Broker Configuration")
    broker_hostname = TextField(label="Broker Hostname", css="col-md-6", error_txt="can only contain numbers and letters.", validation=validate_hostname)
    broker_port = NumberField(label="Broker Port", value=1883, css="col-md-6", error_txt="can only contain numbers")
    broker_username = TextField(label="Broker Username", css="col-md-6")
    broker_password = PasswordField(label="Broker Password", css="col-md-6")
    broker_ssl = CheckboxField(label="Use Secure Socket Layer (SSL)?", value="on", required=False)
    hr_line_2 = LayoutHR(value="Channel Configuration")
    logging_channel = TextField(label="Logging channel", value="fancontrol/logging", css="col-md-4")
    reporting_channel = TextField(label="Reporting channel",value="fancontrol/reporting",css="col-md-4")
    command_channel = TextField(label="Command channel",value="fancontrol/command",css="col-md-4")
    hr_line_3 = LayoutHR()


class MQTTConfiguration(ItemBase):
    _priority = 2
    
    """ wifi configuration class """
    config_attribute = True
    item_name = 'mqtt'
    item_description = 'MQTT Configuration'
    
    def __init__(self, application_configuration, item_configuration):
        log.debug(f'{self.__class__.__name__} started')
        super().__init__(application_configuration, item_configuration)
        self._form = MQTTForm
        
    def process_form(self,session,request):
        form = MQTTForm()
        
        form_dict = request.form
        
        valid, form_list = form.from_form(form_dict)
        
        form_html = form.render(self.item_description, form_list)
        
        import json
        print (json.dumps(form_list))
        return(Template('config_item.html').render(page=self.item_description, application=config, session=session, form=form_html))

        
        
