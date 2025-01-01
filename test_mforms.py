import sys, os
sys.path.append('/Users/brendan/src/fancontrol/lib')

from uforms import BaseForm, TextField, NumberField, PasswordField, CheckboxField, LayoutHR
import uforms.validators as validators

import json

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class MyForm(BaseForm):
    broker_hostname = TextField(label="Broker Hostname", css="col-md-6", error_txt="can only contain numbers and letters.", validation=validators.validate_hostname)
    broker_port = NumberField(label="Broker Port", value=1883, css="col-md-6", error_txt="can only contain numbers")
    broker_username = TextField(label="Broker Username", css="col-md-6")
    broker_password = PasswordField(label="Broker Password", css="col-md-6")
    broker_ssl = CheckboxField(label="Use Secure Socket Layer (SSL)?", value="1", required=False)
    hr_line = LayoutHR()
    logging_channel = TextField(label="Logging channel", value="fancontrol/logging")
    reporting_channel = TextField(label="Reporting channel",value="fancontrol/reporting")
    command_channel = TextField(label="Command channel",value="fancontrol/command")


form_dict = {
            "broker_hostname": "srv4.bgwlan.nl",
            "broker_port": "1",
        }

if __name__ == "__main__":
#     a = Password("brendan", "Bredan!@")
#     number = FormNumber("brendan", "1")
#     print (number.validate())

    template_dir = 'lib/uforms/templates/'
    print (dir(MyForm))
    for fiel in os.listdir(template_dir):
        if fiel.endswith('.py'):
            log.debug(f'removed file {fiel}')
            os.remove(template_dir + fiel)


    
    form = MyForm()
    print ("main")
    
    valid, form_dict = form.from_form(form_dict)
    
    print (json.dumps(form_dict))
    
#     print (form.render("test", form_dict))
    
    
    
#     print (form_list)
#     print(validate_password("test"))
#     vaobj = form.from_form(form_dict)
#     print (json.dumps(form_list))

    
#     print(a.validate())

