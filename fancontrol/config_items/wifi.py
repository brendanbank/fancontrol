import sys
# sys.path.append('/Users/brendan/src/fancontrol/lib')
from uforms import BaseForm, TextField, NumberField, CheckboxField, PasswordField, DisableCheckboxField, LayoutHR
from uforms.validators import validate_hostname
from fancontrol.items import BaseItem

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

class WiFiForm(BaseForm):
    form_description = 'WiFi Configuration'
    hr_line_1 = LayoutHR(value="Access Point Configuration", css="col-md-6", prepend_class="col-md-3", extend_class="col-md-3")
    ap_ssid = TextField(label="Access Point Network Name SSID", css="col-md-6", prepend_class="col-md-3", extend_class="col-md-3")
    ap_password = PasswordField(label="Access Point", css="col-md-6", show_password=True, prepend_class="col-md-3", extend_class="col-md-3")
    hr_line_2 = LayoutHR(css="col-md-6", prepend_class="col-md-3", extend_class="col-md-3")


class WiFiConfiguration(BaseItem):
    """ wifi uconfiguration class """
    _priority = 1    
    item_name = 'wifi'
    
    formcls = WiFiForm
    form_description = WiFiForm.form_description
    
    
    def __init__(self, application_configuration, item_configuration):
        log.debug(f'WiFiConfiguration started')
        super().__init__(application_configuration, item_configuration)
        self.config_ap()
            
    def config_ap(self):
        if not self.item_configuration.ap_ssid:
            self.item_configuration.ap_ssid = self.application_configuration.hostname
        if not self.item_configuration.ap_password:
            self.item_configuration.ap_password = "password"

        
        
            