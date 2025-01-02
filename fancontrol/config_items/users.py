import sys
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
from uforms import BaseForm, TextField, NumberField, CheckboxField, PasswordField, DisableCheckboxField, LayoutHR

from fancontrol.password import hash_password, verify_password
from fancontrol.config import config
from configuration import BaseItem

class ChangePasswordForm(BaseForm):
    form_description = 'User Credentials'
    hr_line_1 = LayoutHR(value="Change Password", css="col-md-6", prepend_class="col-md-3", extend_class="col-md-3")
    password = PasswordField(label="Current Password", css="col-md-6", show_password=True, prepend_class="col-md-3", extend_class="col-md-3")
    new_password = PasswordField(label="New Passwword", css="col-md-6", show_password=True, prepend_class="col-md-3", extend_class="col-md-3")
    hr_line_2 = LayoutHR(value="User Setting", css="col-md-6", prepend_class="col-md-3", extend_class="col-md-3")
    fullname = TextField (label="Full Name",  css="col-md-6", prepend_class="col-md-3", extend_class="col-md-3")
    hr_line_3 = LayoutHR(css="col-md-6", prepend_class="col-md-3", extend_class="col-md-3")


class Users(BaseItem):
    """ user configuration class """
    _priority = 3    
    item_name = 'users'
    item_description = 'User Configuration'
    formcls = ChangePasswordForm
    form_description = formcls.form_description

    def __init__(self, application_configuration, user_config):
        log.debug(f'{self.__class__.__name__} started')
        super().__init__(application_configuration, user_config)
        self.user_config = user_config
        self.check_admin_user()

        
    def check_admin_user(self):
        admin_namespace = self.get_user("admin")
        if not admin_namespace.password:
            self.create_user(admin_namespace,hash_password("admin"))
            
    def get_user(self,username):
        return self.user_config.namespace(username) 
    
    def create_user(self, admin_namespace, password, fullname="John Doe"):
        admin_namespace.password = password
        admin_namespace.fullname = fullname
        
    def verify_username_password(self,username,password):
        user = self.get_user(username)
        if not user:
            return(False)
        else:
            return(verify_password(password,user.password ))
        
    
