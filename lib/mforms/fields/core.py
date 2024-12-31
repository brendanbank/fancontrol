import mforms.validators as validators

class BaseField(object):
    error="cannot be empty."
    
    def __init__(self, *args, **kwargs):
        self._kwargs = kwargs
        self._args = args

        self.name =  kwargs.get('name', "")
        self.value =  kwargs.get('value', "")
        self.label = kwargs.get('label', "")
        self.validation = kwargs.get('validation', validators.default_validation)
        self.css = kwargs.get('css', "col-md-12")
        self.valid = kwargs.get('valid', True)
        self.valid_css = kwargs.get('valid_css', "is-valid")
        self.required = kwargs.get('required', True)
        self.error_txt =  kwargs.get('valid_css', None)

            
        if self.error_txt:
            self.error = self.error_txt


class PasswordField(BaseField):
    type="password"
    error='Password field must contain at least 8 characters has to have one letter and digit and a special characters "[!@#$%^&*(),.?\:{}|<>~_]."'    

class TextField(BaseField):
    type="text"

class NumberField(BaseField):
    type="text"
    error="can only contain numbers."
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation = validators.validate_numbers

class HiddenField(BaseField):
    type="hidden"

class CheckboxField(BaseField):
    type="checkbox"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation = validators.validate_true
