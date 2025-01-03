import re
import logging
import json
import os
import types
import uforms.validators
from uforms.fields.core import BaseField, DisableCheckboxField
from uforms.fields.layout import LayoutBase
from uforms import Template
import utemplate



logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def _get_template_path(path):
    template_dir = f'{path}/templates'
    cwd_path = os.getcwd() + '/'
    template_dir = template_dir.replace(cwd_path,"")
    log.debug(f'template_dir = {template_dir}')
    return(template_dir)

def _remove_old_compiled_templates(directory):
    directory += "/"
    log.debug(f'clean directry: {directory} with compiled templates')
    for fiel in os.listdir(directory):
        if fiel.endswith('.py'):
            log.debug(f'removed files {directory}{fiel}')
            os.remove(directory + fiel)

def initialize(recompile = False):
    if recompile:
        _remove_old_compiled_templates(uforms.template_dir)
#         _remove_old_compiled_templates(uforms.template_dir + "/fields")
#         fields_dir = f'{uforms.template_dir}/fields'
#         loader = utemplate.source.Loader(None, fields_dir)
#         for f in os.listdir(fields_dir):
#             if f.endswith(".py"):
#                 continue
#             fname = fields_dir + "/" + f
#             log.debug(f'compile: {fname}')
#             loader.load(f)

class BaseForm(object):

    form_description = "form_description = empty"

    def __init__(self, css=""):
        self.css = css
        self.disable_id = None
        self.form_items = {}
        self._order = list()
        self._form_fields = list()
        self._class_args = list()
        self._cls = None
        self.name = self.__class__.__dict__
        
        self._fill_self()
        
#         self._create_empty_class()
        
    def _fill_self(self):
        for cls_attribute in dir(self):
            try:
                obj = getattr(self.__class__, cls_attribute)
            except:
                continue

            if issubclass(obj.__class__, BaseField):
                
                clsobj = getattr(self, cls_attribute)
                setattr(clsobj, 'name', cls_attribute)                
                self.form_items[cls_attribute] = clsobj
                
                disabled_checkbox =  getattr (clsobj, "disable_checkbox", None)
                
                if disabled_checkbox:
                    self.disable_id = cls_attribute
                    
                if not issubclass(obj.__class__, LayoutBase):
                    self._form_fields.append(cls_attribute)
                
                
                
                
                clsobj.name = cls_attribute
                
        
        for clsobj in sorted(self.form_items.values() , key=lambda k: k._field_order):
            self._order.append(clsobj.name)

                
    def validate_form(self, form):
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
                log.debug(f'attribue {name} ({obj.__class__.__name__}) valid: True')
                
            elif form and form.get(name):
                
                field_dict['value'] = form.get(name)
                                
                if obj.validation:
                    field_dict['valid'] = obj.validation(form.get(name))
                    log.debug(f'validation on attribue {name} ({obj.__class__.__name__}) valid: {field_dict['valid']}')

                    
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
        log.debug(f'validation from_form {valid}')
        return(valid, form_list)
        
    def create_dict_from_named_fields(self, strorage_dict, form_fields):
        field_dict = {}
        for field_name in form_fields:
            print (strorage_dict)
            value = strorage_dict.get(field_name)
            if not value == None:
                field_dict[field_name] = value
        return field_dict

    def render(self, header, form_dict):
        return(Template('form.html').render(header=header, form=form_dict))

    def process_form(self, current_settings, session, request):
                
        form_dict = {
            'name': self.__class__.__name__,
            'fields': list(),
            'alert': False,
            'alert_type': "success",
            'disable_id': self.disable_id
        }
                
        form_fields = self._form_fields
        
        field_dict = {}
        field_dict['enable'] = "on"
        
        if request.method == "GET":  # fetch current settings
            print (current_settings)
            field_dict = self.create_dict_from_named_fields(current_settings, form_fields)
            
        elif request.method == "POST" and request.form and not request.form.get('submit') == None and len(request.form) == 1:
            current_settings['enable'] = "off"  # dusabked checkbox is set
            field_dict['enable'] = "off"
            field_dict = self.create_dict_from_named_fields(current_settings, form_fields)
            form_dict['alert'] = f"{self.form_description} was disabled!"
            form_dict['alert_type'] = "warning"
            
        else:
            for field_name in request.form.keys():
                field_dict[field_name]  = request.form[field_name]
                
            print (field_dict)
            
        log.debug(f'field_dict: {field_dict}')
        
        valid, fields_list = self.validate_form(field_dict)

        if request.method == "POST" and valid and field_dict.get('enable') == "on":
            for field_name in self._form_fields:
                current_settings[field_name] =  request.form.get(field_name, False)
                
            form_dict['alert'] = f"{self.form_description} was successfully saved!"

        form_dict['fields'] = fields_list
        form_html = self.render(self.form_description, form_dict)
        return form_html

