import sys
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

from fancontrol.password import hash_password, verify_password
from fancontrol.config import config
from configuration import ItemBase

class Users(ItemBase):
    """ user configuration class """
    _priority = 3    
    item_name = 'users'
    item_description = 'User Configuration'
    
    def __init__(self, application_configuration, user_config):
        log.debug(f'{self.__class__.__name__} started')
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
        
    
