import sys, os, ssl
import asyncio

sys.path.append('/Users/brendan/src/fancontrol/lib')

try:
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("BGWLAN", "Hans&Paul1")
    print("IP Address:", wlan.ifconfig()[0])

except:
    pass

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

from microdot import Microdot, Response, send_file, abort
from microdot.utemplate import Template
from microdot.session import Session, with_session

from utemplate import recompile
from config import config
import config as config_obj



app = Microdot()
config_obj.app_obj = app

from microdot_login import authorization_required, admin_login

Session(app, secret_key=config.app_password)
Response.default_content_type = 'text/html'
Template.initialize(loader_class=recompile.Loader)

@app.route('/')
@with_session
@authorization_required
async def index(req, session):
    print (session)
    return Template('index.html').render(page='Home',application=config, session=session)

@app.route('/static/<path:path>')
@with_session
async def static(request, session, path):
    try:
        os.stat(f'static/{path}.gz')
    except OSError:
        log.error (f'file static/{path}.gz not found!')
        abort(404, reason="File not found")
    return send_file('static/' + path, compressed=True, file_extension='.gz', max_age=(3600))

@app.route('/settings/<string:setting_name>', methods=['GET', 'POST'])
@authorization_required
async def setting_name(request, setting_name):
    session = request.app._session.get(request)
    return Template('wifi.html').render(page='Network Configuration Settings', application=config, session=session)

async def task():
    ext="der"
    logging.basicConfig(level=logging.INFO)
    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.verify_mode = ssl.CERT_NONE
    sslctx.load_cert_chain(certfile='cert/cert.der', keyfile = 'cert/key.' + ext)
    await app.start_server(host="0.0.0.0", port=5999, debug=True)
#     await app.start_server(host="0.0.0.0", port=5999, debug=True, ssl=sslctx)

if __name__ == '__main__':
    asyncio.run(task())
