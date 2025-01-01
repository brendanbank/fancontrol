from uforms.fields.core import BaseField
from uforms import validators


class LayoutBase(BaseField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation = validators.validate_true
        self.required = False
        self.fullwidth = False

class LayoutHR(LayoutBase):
    type="hr"
    error=''
    value="<hr>"
    