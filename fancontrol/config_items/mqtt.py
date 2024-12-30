import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import logging
log = logging.getLogger(__name__)
import re

from fancontrol.config import config
from configuration import ItemBase
from fancontrol.formitems import FormBase, FormText, FormNumber, FormCheckbox, validate_hostname, FormPassword
from microdot.utemplate import Template

def validate_hostname(hostname):
    ValidHostnameRegex="^[\w\.-]+$"
    regex = re.compile(ValidHostnameRegex)
    log.debug(f'validate {hostname}: {regex.search(hostname)}')
    return True if regex.search(hostname) else False

class MQTTForm(FormBase):
    broker_hostname = FormText(label="Broker Hostname", css="col-md-6", error_txt="can only contain numbers and letters.", validation=validate_hostname)
    broker_port = FormNumber(label="Broker Port", value=1883, css="col-md-6", error_txt="can only contain numbers")
    broker_username = FormText(label="Broker Username", css="col-md-6")
    broker_password = FormPassword(label="Broker Password", css="col-md-6")
    broker_ssl = FormCheckbox(label="Use Secure Socket Layer (SSL)?", value="1", required=False)
    logging_channel = FormText(label="Logging channel", value="fancontrol/logging", css="col-md-6")
    reporting_channel = FormText(label="Reporting channel",value="fancontrol/reporting")
    command_channel = FormText(label="Command channel",value="fancontrol/command")

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
        form = self._form().newInstance()        
        form_dict = request.form
        valid, form_list = form.from_form(form_dict)
        import json
        print (json.dumps(form_list))
        return(Template('form.html').render(page=self.item_description, application=config, session=session, form=form_list))

        
        
