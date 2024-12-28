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
    config_description = 'User Configuration'
    
    
    def __init__(self, application_configuration, user_config):
        log.debug(f'{self.__class__.__name__} started')
        self.user_config = user_config
        if not user_config.usernames:
            user_config.usernames = dict()
        self.check_admin_user()
        
    def check_admin_user(self):
        if not self.get_user('admin'):
            self.create_user('admin',hash_password("admin"))
            
    def get_user(self,username):
        usernames = self.user_config.usernames
        return usernames.get(username) 
    
    def create_user(self, username, password, fullname="John Doe"):
        usernames = self.user_config.usernames
        usernames[username] = {}
        usernames[username]["password"] = password
        usernames[username]["fullname"] = fullname
        
    def verify_username_password(self,username,password):
        user = self.get_user(username)
        if not user:
            return(False)
        else:
            return(verify_password(password,user['password'] ))
        
    
