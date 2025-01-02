from microdot import redirect, send_file, abort
from microdot.session import Session, with_session
from microdot.utemplate import Template
from fancontrol.views.login_view import authorization_required, admin_login
import os
import logging
log = logging.getLogger(__name__)

from fancontrol.config import app, config, factory

log.debug (f'add route / {app}')

@app.route('/')
@with_session
@authorization_required
async def index(req, session):
    return Template('index.html').render(page='Home', factory=factory, application=config, session=session)

@app.route('/static/<path:path>')
@with_session
async def static(request, session, path):
    
    try:
        os.stat(f'fancontrol/static/{path}')
        return send_file('fancontrol/static/' + path , max_age=(3600))
    except OSError:
        log.error (f'file static/{path} not found!')

    try:
        os.stat(f'fancontrol/static/{path}.gz')
    except OSError:
        log.error (f'file static/{path}.gz not found!')
        abort(404, reason="File not found")
    return send_file('fancontrol/static/' + path, compressed=True, file_extension='.gz', max_age=(3600))

@app.route('favicon.ico')
async def static_ico(request):
    
    favicon = 'fancontrol/static/favicon.ico'
    
    try:
        os.stat(favicon)
        return send_file(favicon , max_age=(3600))
    except OSError:
        log.error (f'file {favicon} not found!')
        abort(404, reason="File not found")
        
    return send_file(favicon , compressed=True, max_age=(3600))
