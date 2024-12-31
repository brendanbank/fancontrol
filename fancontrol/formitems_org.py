import re
import logging
import json
import types

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def default_validation(value):
    return True

class FormItemBase(object):
    error="cannot be empty."
    default_arguments = {
                            'name': "",
                            'value': "",
                            'label': None,
                            'validation': default_validation,
                            'css': "col-md-12",
                            'valid': True,
                            'valid_css': "is-valid",
                            'required': True,
                            'error_txt': None
                        }
    
#     def __init__(self,
#                  name=None,
#                  value="",
#                  label=None,
#                  validation=default_validation,
#                  css="col-md-12",
#                  valid_css = "is-valid",
#                  required = True,
#                  error_txt=None,
#                  *args, **kwargs):

    def __init__(self, *args, **kwargs):
        log.debug(f'called with *args: {args}, **kwargs:{kwargs}')
        
        self._kwargs = kwargs
        self._args = args
        
        for key, value in self.default_arguments.items():
            setattr(self,key,value)
            
        for key, value in kwargs.items():
            setattr(self,key,value)
            
        if self.error_txt:
            self.error = self.error_txt
            
def validate_password(password):
    """
    Validates a password to ensure it has at least:
    - One letter (lowercase or uppercase)
    - One digit
    - One punctuation character

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    
    has_letter = re.search(r'[a-zA-Z]', password)  # At least one letter
    has_digit = re.search(r'\d', password)        # At least one digit
    has_punctuation = re.search(r'[!@#$%^&*(),.?":{}|<>~`_]', password)  # Punctuation
    has_whitespace = re.search(r'\s', password)
    
    if has_letter and has_digit and has_punctuation and not has_whitespace and len(password) > 8:
        log.debug(f'validate {password}: True')
        return True
    log.debug(f'validate {password}: False')
    return False

class FormPassword(FormItemBase):
    type="password"
    error='Password field must contain at least 8 characters has to have one letter and digit and a special characters "[!@#$%^&*(),.?\:{}|<>~_]."'    

    
class FormText(FormItemBase):
    type="text"


def validate_numbers(value):
    regex = re.compile("^\d+$")
    return True if regex.search(value) else False

class FormNumber(FormItemBase):
    type="text"
    error="can only contain numbers."
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation = validate_numbers

class FormHidden(FormItemBase):
    type="hidden"

def validate_true(value):
    return (True)

class FormCheckbox(FormItemBase):
    type="checkbox"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation = validate_true


class FormBase(object):
    def __init__(self, css=""):
        self.css = css
        self.form_items = {}
        self._order = list()
        self._class_args = list()
        self._cls = None
        
        self._fill_self()
        self._create_empty_class()
        
        
    def _fill_self(self):
        for cls_attribute in dir(self):
            try:
                obj = getattr(self.__class__, cls_attribute)
            except:
                continue

            if issubclass(obj.__class__, FormItemBase):
                self._order.append(cls_attribute)
                clsobj = getattr(self, cls_attribute)
                setattr(clsobj, 'name', cls_attribute)
                
#                 obj.name = cls_attribute
                
                print (clsobj)
                
                self.form_items[cls_attribute] = clsobj
                
                clsobj._kwargs['name'] = cls_attribute
                
                self._class_args.append(
                                    {'_name': cls_attribute,
                                     '_args': clsobj._args ,
                                     '_kwargs': clsobj._kwargs,
                                     '_cls': obj.__class__
                                })

    def _create_empty_class(self):
        
        name = 'Dynamnic' + self.__class__.__name__
        
        def clsexec(ns):
            attrs = []
            ns['type'] = name
            ns['attrs'] = attrs
            
        self._cls = types.new_class(name, bases=(FormBase,), exec_body=clsexec)


    def newInstance(self):
        new_formbase = FormBase()
        log.debug (self.__class__.__name__)
        
        clsobj = self._cls()
        
        for form_item in self._class_args:
            setattr(clsobj, form_item['_name'], form_item['_cls'](*form_item['_args'],**form_item['_kwargs']) )
        
        clsobj.css = self.css
        clsobj.form_items = self.form_items
        clsobj._order = self._order
        clsobj._class_args = self._class_args
        clsobj._cls = self._cls
    
        return(clsobj)
        
    def from_form(self, form):
        self.form_list = list()
        valid = True
        form_list = list()
        default_valid = True
        if  form:
            default_valid = False
            
        for name in self._order:
            obj = getattr(self,name)
        
            if form and form.get(name):
                
                obj.value = form.get(name)
                                
                if obj.validation:
                    obj.valid = obj.validation(form.get(name))
                    
                if not obj.valid:
                    valid = False
                    obj.valid_css = "is-invalid"
            elif form and not form.get(name) and obj.type == "checkbox":
                obj.value = "off"
            else: 
                obj.valid = default_valid
                valid = False
                
            form_list.append({
                "type": obj.type,
                "name": obj.name,
                "label": obj.label,
                "valid": obj.valid,
                "value": obj.value,
                "error": obj.error,
                "valid_css":  obj.valid_css,
                "css": obj.css,
                "required": obj.required
                })
        
        return(valid, form_list)
        


def validate_hostname(hostname):
    ValidHostnameRegex="^[\w\.-]+$"
    regex = re.compile(ValidHostnameRegex)
    log.debug(f'validate {hostname}: {regex.search(hostname)}')
    return True if regex.search(hostname) else False

class MyForm(FormBase):
    broker_hostname = FormText(label="Broker Hostname", css="col-md-6", error_txt="can only contain numbers and letters.", validation=validate_hostname)
    broker_port = FormNumber(label="Broker Port", value=1883, css="col-md-6", error_txt="can only contain numbers")
    broker_username = FormText(label="Broker Username", css="col-md-6")
    broker_password = FormPassword(label="Broker Password", css="col-md-6")
    broker_ssl = FormCheckbox(label="Use Secure Socket Layer (SSL)?", value="1", required=False)
    logging_channel = FormText(label="Logging channel", value="fancontrol/logging")
    reporting_channel = FormText(label="Reporting channel",value="fancontrol/reporting")
    command_channel = FormText(label="Command channel",value="fancontrol/command")


form_dict = {
            "broker_hostname": "srv4.bgwlan.nl",
            "broker_port": "1",
        }

if __name__ == "__main__":
#     a = Password("brendan", "Bredan!@")
#     number = FormNumber("brendan", "1")
#     print (number.validate())
    print ("main")
    form = MyForm()
    new_instance = form.newInstance()
    
    valid, form_dict = new_instance.from_form(form_dict)
    
    print (json.dumps(form_dict))
    
#     print (form_list)
#     print(validate_password("test"))
#     vaobj = form.from_form(form_dict)
#     print (json.dumps(form_list))

    
#     print(a.validate())
