import os, logging
from utemplate import recompile
from uforms.utemplate import Template
from uforms.uforms import BaseForm
from uforms.uforms import _get_template_path
from uforms.uforms import initialize

from uforms.fields.core import TextField
from uforms.fields.core import NumberField
from uforms.fields.core import PasswordField
from uforms.fields.core import CheckboxField
from uforms.fields.core import DisableCheckboxField


from uforms.fields.layout import LayoutHR




log = logging.getLogger(__name__)

# Template.initialize(loader_class=recompile.Loader, template_dir=template_dir)

    
template_dir = _get_template_path(__path__)


Template.initialize(template_dir=template_dir)
