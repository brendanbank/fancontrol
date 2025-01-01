import os, logging
from utemplate import recompile
from uforms.utemplate import Template
from uforms.uforms import BaseForm
from uforms.fields.core import TextField
from uforms.fields.core import NumberField
from uforms.fields.core import PasswordField
from uforms.fields.core import CheckboxField
from uforms.fields.core import DisableCheckboxField


from uforms.fields.layout import LayoutHR




log = logging.getLogger(__name__)

# Template.initialize(loader_class=recompile.Loader, template_dir=template_dir)

def _get_template_path():
    template_dir = f'{__path__}/templates'
    cwd_path = os.getcwd() + '/'
    template_dir = template_dir.replace(cwd_path,"")
    return(template_dir)

def _remove_old_compiled_templates(directory):
    directory += "/" 
    for fiel in os.listdir(directory):
        if fiel.endswith('.py'):
            log.debug(f'removed file {directory}{fiel}')
            os.remove(directory + fiel)

template_dir = _get_template_path()

_remove_old_compiled_templates(f'{__path__}/templates')

Template.initialize(template_dir=template_dir)
