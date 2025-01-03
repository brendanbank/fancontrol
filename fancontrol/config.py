import sys, os
import ubinascii
import logging

from microdot import Microdot, Response
from uconfiguration import Configuration
from fancontrol.items import ItemFactory
from fancontrol.password import generate_password, hash_password
from microdot.session import Session
from microdot.utemplate import Template
from microdot.cors import CORS
from utemplate import recompile
from fancontrol.ws_types import BoundedList, WebSocketHandler

from uconfiguration.storage.json import JsonStorage

storage = JsonStorage(configfile="config.json")
config = Configuration(storage)
config.load_config()

# configure logging
websocket_logging_list = BoundedList(10)
logging.getLogger().addHandler(WebSocketHandler(websocket_logging_list))


application_name = "Fan Control"
app = Microdot()
CORS(app, allowed_origins=['http://127.0.0.1:5999/logging'], allow_credentials=True)


saveconfig = False

if config.application_name == None:
    config.application_name = application_name

if config.app_password == None:
    config.app_password = generate_password(24)

if config.hostname == None:
    try:
        import marchine
        config.hostname = f'{config.application_name} {ubinascii.hexlify(machine.unique_id()).decode()[-4:]}'
    except:
        config.hostname = f'{config.application_name} {ubinascii.hexlify(os.urandom(4)).decode()}'

factory = ItemFactory('fancontrol/config_items', config)

config.save_config()

try:
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("BGWLAN", "Hans&Paul1")
    print("IP Address:", wlan.ifconfig()[0])

except:
    pass

template_dir = 'fancontrol/templates/'

Session(app, secret_key=config.app_password)
Response.default_content_type = 'text/html'
Template.initialize(loader_class=recompile.Loader, template_dir=template_dir)
