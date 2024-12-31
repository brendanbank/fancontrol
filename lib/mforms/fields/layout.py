from mforms.fields.core import BaseField


class LayoutBase(BaseField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required = False

class LayoutHR(LayoutBase):
    type="hr"
    error=''
    value="<hr>"
    