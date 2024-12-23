import sys, os, ssl
sys.path.append('/Users/brendan/src/fancontrol/lib')

try:
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("BGWLAN", "Hans&Paul1")
    print("IP Address:", wlan.ifconfig()[0])

except:
    pass

from microdot import Microdot, Response, send_file, abort
from microdot.utemplate import Template
from utemplate import recompile
import ulogging as logging

log = logging.getLogger(__name__)

app = Microdot()
Response.default_content_type = 'text/html'

Template.initialize(loader_class=recompile.Loader)
    
application_vars = {}
application_vars["application_name"] = "Fan Control"


@app.route('/static/<path:path>')
async def static(request, path):
    try:
        os.stat(f'static/{path}.gz')
    except OSError:
        log.error (f'file static/{path}.gz not found!')
        abort(404, reason="File not found")
    return send_file('static/' + path, compressed=True, file_extension='.gz', max_age=(3600))

@app.route('/')
async def index(req):
    return Template('index.html').render(page='Home',application=application_vars)

@app.route('/settings/<string:setting_name>', methods=['GET', 'POST'])
async def setting_name(req, setting_name):
    print (f'req form = {req.form}')
    return Template('wifi.html').render(page='Network Configuration Settings', application=application_vars)


if __name__ == '__main__':
    ext="der"
    logging.basicConfig(level=logging.INFO)
    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.load_cert_chain(certfile='cert/cert.der', keyfile = 'cert/key.' + ext)
    
    app.run(port=5999, debug=True)
#     app.run(port=5999, debug=True, ssl=sslctx)
