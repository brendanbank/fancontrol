
from configuration import Configuration
from password import generate_password

DICT_OBJ = dict ()
config = Configuration(DICT_OBJ, configfile="/Users/brendan/src/fancontrol/config.json")

application_name = "Fan Control"

saveconfig = False

if config.application_name == None:
    config.application_name = application_name
    saveconfig = True

if config.app_password == None:
    config.app_password = generate_password(24)
    saveconfig = True

if saveconfig:
    config.save_config()