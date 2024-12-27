from configuration import Configuration
from password import generate_password

DICT_OBJ = dict ()

config = Configuration(DICT_OBJ, configfile="/Users/brendan/src/fancontrol/config.json")

application_name = "Fan Control"
app_obj = None

saveconfig = False

if config.application_name == None:
    config.application_name = application_name

if config.app_password == None:
    config.app_password = generate_password(24)

if config.password == None:
    config.password = "admin"

if config.username == None:
    config.username = "admin"

try:
    import ubinascii
    import marchine
    if config.hostname == None:
        config.hostname = ubinascii.hexlify(machine.unique_id()).decode()
except:
    config.hostname = config.application_name

config.config_to_factory()
config.save_config()