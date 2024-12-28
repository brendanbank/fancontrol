from microdot import redirect, send_file, abort
from microdot.session import Session, with_session
from microdot.utemplate import Template
from fancontrol.views.login_view import authorization_required, admin_login
import os
import logging
log = logging.getLogger(__name__)

from fancontrol.config import app, config

log.debug (f'add route / {app}')

@app.route('/')
@with_session
@authorization_required
async def index(req, session):
    return Template('index.html').render(page='Home', application=config, session=session)

@app.route('/static/<path:path>')
@with_session
async def static(request, session, path):
    try:
        os.stat(f'fancontrol/static/{path}.gz')
    except OSError:
        log.error (f'file static/{path}.gz not found!')
        abort(404, reason="File not found")
    return send_file('fancontrol/static/' + path, compressed=True, file_extension='.gz', max_age=(3600))

@app.route('/settings/<string:setting_name>', methods=['GET', 'POST'])
@authorization_required
async def setting_name(request, setting_name):
    session = request.app._session.get(request)
    return Template('wifi.html').render(page='Network Configuration Settings', application=config, session=session)
