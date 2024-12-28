import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import logging


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

from fancontrol.login import hash_password

from fancontrol.config import config


class Uses(object):
    def __init__(self, username, users_config):
        pass

class Users():
    def __init__(self, user_config):
        self.user_config = user_config
        if not user_config.usernames:
            user_config.usernames = dict()
        
    def get_user(self,username):
        usernames = self.user_config.usernames
        
        return(usernames.get(username, None))
    
    def create_user(self, username, password, fullname="John Doe"):
        usernames = self.user_config.usernames
        usernames[username] = {}
        usernames[username]["password"] = password
        usernames[username]["fullname"] = fullname

if __name__ == "__main__":
    namespace = config.namespace("users")
    users = Users(namespace)
    if not users.get_user('brendan'):
        users.create_user('brendan',hash_password("very secret"))
    
    print (config._storage)
    
    print (users.get_user('brendan'))
        