import uforms.validators as validators

class BaseField(object):
    error="cannot be empty."
    
    def __init__(self, *args, **kwargs):
        self._kwargs = kwargs
        self._args = args
        self.additional_attributes = {}

        self.name =  kwargs.get('name', "")
        self.value =  kwargs.get('value', "")
        self.label = kwargs.get('label', "")
        self.validation = kwargs.get('validation', validators.default_validation)
        self.css = kwargs.get('css', "col-md-12")
        self.valid = kwargs.get('valid', True)
        self.valid_css = kwargs.get('valid_css', "is-valid")
        self.required = kwargs.get('required', True)
        self.error_txt =  kwargs.get('valid_css', None)
        self.extend_class =  kwargs.get('extend_class', None)
        self.prepend_class =  kwargs.get('prepend_class', None)

            
        if self.error_txt:
            self.error = self.error_txt


class PasswordField(BaseField):
    type="password"
    error='Password field must contain at least 8 characters has to have one letter and digit and a special characters "[!@#$%^&*(),.?\:{}|<>~_]."'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('show_password'):
            self.additional_attributes.update({ 'show_password': True })


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
        self.additional_attributes.update({ 'checkbox_css': "" })


class DisableCheckboxField(BaseField):
    type="checkbox"
    disable_checkbox = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation = validators.validate_true
        self.additional_attributes.update({ 'checkbox_css': " disable-button" })
        
    
    
    
