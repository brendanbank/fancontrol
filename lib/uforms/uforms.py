import re
import logging
import json
import types
import uforms.validators
from uforms.fields.core import BaseField, DisableCheckboxField
from uforms.fields.layout import LayoutBase
from uforms import Template


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class BaseForm(object):
    def __init__(self, css=""):
        self.css = css
        self.disable_id = None
        self.form_items = {}
        self._order = list()
        self._form_configuration_fields = list()
        self._class_args = list()
        self._cls = None
        self.name = self.__class__.__name__
        
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
                self._order.append(cls_attribute)
                clsobj = getattr(self, cls_attribute)
                setattr(clsobj, 'name', cls_attribute)                
                self.form_items[cls_attribute] = clsobj
                
                disabled_checkbox =  getattr (clsobj, "disable_checkbox", None)
                
                if disabled_checkbox:
                    self.disable_id = cls_attribute
                    
                if not issubclass(obj.__class__, LayoutBase):
                    self._form_configuration_fields.append(cls_attribute)
                
                
                
                
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
                "extend_class": obj.extend_class,
                "prepend_class": obj.prepend_class,
                "required": obj.required
                }

            if issubclass(obj.__class__, LayoutBase):
                field_dict['valid'] = True
                
            elif form and form.get(name):
                
                field_dict['value'] = form.get(name)
                                
                if obj.validation:
                    field_dict['valid'] = obj.validation(form.get(name))
                    
                if not field_dict['valid']:
                    valid = False
                    field_dict['valid_css'] = "is-invalid"
            
            elif form and not form.get(name) and obj.type == "checkbox" and not form.get('enable') == "off":
                field_dict['value'] = "off"
                
            else:
                field_dict['valid'] = default_valid
                valid = False
            

            field_dict.update(obj.additional_attributes)            

            form_list.append(field_dict)
        
        return(valid, form_list)
        


