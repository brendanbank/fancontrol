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
from microdot_login import authorization_required

from utemplate import recompile

from config import config


app = Microdot()
Session(app, secret_key=config.app_password)
Response.default_content_type = 'text/html'
Template.initialize(loader_class=recompile.Loader)

@app.route('/')
@with_session
@authorization_required
async def index(req, session):
    return Template('index.html').render(page='Home',application=config)

@app.route('/test')
async def test(request):
    
    fields = [
            {
                'name': 'ssid',
                'text': 'SSID',
                'type': "text",
                'columns': "col-sm-6",
                'error': False,
                'error_txt': 'Valid SSID is required.',
                'value': ""
            },
            {
                'name': "password",
                'text': "Password",
                'type': "password",
                'columns': "col-sm-6",
                'error': True,
                'error_txt': 'Valid password is required.',
                'value': ""
            },
            {
                'name': "hostname",
                'text': "Hostname",
                'type': "text",
                'columns': "col-12",
                'error': False,
                'error_txt': 'Please enter a Device Name (no spaces or special characters allowed).',
                'value': "hostname"
            },
        ]

    return Template('test.html').render(page='Test',application=config, form_fields=fields)


@app.route('/static/<path:path>')
async def static(request, path):
    try:
        os.stat(f'static/{path}.gz')
    except OSError:
        log.error (f'file static/{path}.gz not found!')
        abort(404, reason="File not found")
    return send_file('static/' + path, compressed=True, file_extension='.gz', max_age=(3600))


@app.route('/settings/<string:setting_name>', methods=['GET', 'POST'])
async def setting_name(req, setting_name):
    print (f'req form = {req.form}')
    return Template('wifi.html').render(page='Network Configuration Settings', application=config)

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
#     ext="der"
#     logging.basicConfig(level=logging.INFO)
#     sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#     sslctx.verify_mode = ssl.CERT_NONE
#     sslctx.load_cert_chain(certfile='cert/cert.der', keyfile = 'cert/key.' + ext)
#     
# #     app.run(port=5999, debug=True)
# 
# 
#     app.run(port=5999, debug=True, ssl=sslctx)
