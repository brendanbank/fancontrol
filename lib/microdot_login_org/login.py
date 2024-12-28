from microdot import redirect
from microdot.session import Session, with_session
from microdot.utemplate import Template
from microdot.helpers import wraps
from microdot.microdot import invoke_handler
import logging
log = logging.getLogger(__name__)

from config import config
import config as config_obj

app = config_obj.app_obj

def login_redirect(req):
    
    referrer = req.url

    if req.query_string and req.query_string.get("url"):
        referer = req.query_string.get("url")
        
    log.debug(f'referrer = {referrer}')
    return (redirect(f'/login?url={referrer}'))

def authorization_required(f):
    @wraps(f)
    async def wrapper(request, *args, **kwargs):
        session = request.app._session.get(request)
        log.debug (f'authorization_required called with session {session}')
        if not session.get('username'):
            log.debug(f'auth failed')
            return await invoke_handler(
                login_redirect, request)
        
        log.debug(f'auth succes for username = {session.get("username")}')
        print (args)
        return await invoke_handler(
            f, request, *args, **kwargs)
        
    return wrapper

def admin_login(request, session):
    
    log.debug (f'admin_login called with session {session} and form {request.form}')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if request.form and username == config.username and password == config.password:
            log.info(f'user {username} logged in.')
            session['username'] = request.form.get('username')
            session.save()
            print (request.args)
            return (redirect(request.args.get("url","/")))
        else:
            log.critical(f'login failed for user {username}')

    return Template('login.html').render(page='Login',application=config, session=session)

def admin_logout(request, session):
    del(session['username'])
    session.save()
    return (redirect('/'))

@app.route('/login', methods=['GET', 'POST'])
@with_session
async def login(request, session):
    return admin_login(request, session)

@app.route('/logout', methods=['GET', 'POST'])
@with_session
@authorization_required
async def logout(request, session):
    return admin_logout(request, session)

    
    

