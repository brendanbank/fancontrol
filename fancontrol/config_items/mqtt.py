import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import logging
log = logging.getLogger(__name__)
import re

from fancontrol.config import config
from configuration import ItemBase
from uforms import BaseForm, TextField, NumberField, CheckboxField, PasswordField, DisableCheckboxField, LayoutHR
from uforms.validators import validate_hostname
from microdot.utemplate import Template

def validate_hostname(hostname):
    ValidHostnameRegex="^[\w\.-]+$"
    regex = re.compile(ValidHostnameRegex)
    log.debug(f'validate {hostname}: {regex.search(hostname)}')
    return True if regex.search(hostname) else False

class MQTTForm(BaseForm):
    enable = DisableCheckboxField(label="Enable MQTT", value="on", required=False)
    hr_line_1 = LayoutHR(value="Broker Configuration")
    broker_hostname = TextField(label="Broker Hostname", css="col-md-6", error_txt="can only contain numbers and letters.", validation=validate_hostname)
    broker_port = NumberField(label="Broker Port", value=1883, css="col-md-6", error_txt="can only contain numbers")
    broker_username = TextField(label="Broker Username", css="col-md-6")
    broker_password = PasswordField(label="Broker Password", css="col-md-6", show_password=True)
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
        
        form = self._form()
        
        form_dict = {
            'name': form.name,
            'fields': list(),
            'success': False,
            'disable_id': form.disable_id
        }
        
        item_configuration = self.item_configuration
        config_fields = form._form_configuration_fields
        
        config_dict = {}
        config_dict['enable'] = "on"
        
        if request.method == "GET": # fetch current settings        
            config_dict = item_configuration.create_dict_from_config(config_fields)
            
        elif request.method == "POST" and request.form and not request.form.get('submit') == None and len(request.form) == 1:
            self.item_configuration.enable = "off" # dusabked checkbox is set
            config_dict['enable'] = "off"
            config_dict = item_configuration.create_dict_from_config(config_fields)
            
        else:
            config_dict = request.form
        
        valid, fields_list = form.from_form(config_dict)

        if request.method == "POST" and valid and config_dict['enable'] == "on":
            for field_name in form._form_configuration_fields:
                setattr(self.item_configuration, field_name, request.form.get(field_name, False))
            form_dict['success'] = f"{__class__.item_description} was successfully saved!"

        form_dict['fields'] = fields_list
        form_html = form.render(self.item_description, form_dict)
        config.save_config()
        return(Template('config_item.html').render(page=self.item_description, application=config, session=session, form=form_html))

        
        
