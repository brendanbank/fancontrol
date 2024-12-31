import re
import logging
import json
import types
import mforms.validators
from mforms.fields.core import BaseField
from mforms import Template


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class BaseForm(object):
    def __init__(self, css=""):
        self.css = css
        self.form_items = {}
        self._order = list()
        self._class_args = list()
        self._cls = None
        
        self._fill_self()
#         self._create_empty_class()

    def render(self, header, form_dict):
        return(Template('form.tmpl').render(header=header, form=form_dict))
        
    def _fill_self(self):
        for cls_attribute in dir(self):
            try:
                obj = getattr(self.__class__, cls_attribute)
            except:
                continue

            if issubclass(obj.__class__, BaseField):
                print (cls_attribute)
                self._order.append(cls_attribute)
                clsobj = getattr(self, cls_attribute)
                setattr(clsobj, 'name', cls_attribute)                
                
                self.form_items[cls_attribute] = clsobj
                
                clsobj.name = cls_attribute
                
    def from_form(self, form):
        self.form_list = list()
        valid = True
        form_list = list()
        default_valid = True
        if  form:
            default_valid = False
            
        for name in self._order:
            obj = getattr(self,name)

            field_dict = {
                "type": obj.type,
                "name": obj.name,
                "label": obj.label,
                "valid": obj.valid,
                "value": obj.value,
                "error": obj.error,
                "valid_css":  obj.valid_css,
                "css": obj.css,
                "required": obj.required
                }

            if form and form.get(name):
                
                field_dict['value'] = form.get(name)
                                
                if obj.validation:
                    field_dict['valid'] = obj.validation(form.get(name))
                    
                if not field_dict['valid']:
                    valid = False
                    field_dict['valid_css'] = "is-invalid"
                    
            elif form and not form.get(name) and obj.type == "checkbox":
                field_dict['value'] = "off"
            else: 
                field_dict['valid'] = default_valid
                valid = False
                
            form_list.append(field_dict)
        
        return(valid, form_list)
        


