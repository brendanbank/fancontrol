import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
from uconfiguration import Configuration

import logging
log = logging.getLogger(__name__)


if __name__ == "__main__":
    from uconfiguration.storage.json import JsonStorage
    logging.basicConfig(level=logging.DEBUG)
    storage = JsonStorage(configfile="config-dev.json")
    
    
    config = Configuration(storage)
    config.load_config()
    
    print (storage._has_changed(storage._storage))
    config.a = 1
    # config["b"] = 2
    print (storage._has_changed(storage._storage))
    
    
    namespace_users = config.namespace("user")
    
    log.debug (namespace_users)

    users = namespace_users.namespace("users")
    brendan = users.namespace("brendan")
    print (brendan.password)
    
#     brendan.password = "test"
#     brendan.username = "Brendan Bank"
    
    config.save_config()
    
    # config["b"] = 2
    # log.debug (config.b)
    #
    # log.debug (config.get("b"))
    #
    #
    # namespace_test.changes = True
    # print (config)
    # print (namespace_test)
