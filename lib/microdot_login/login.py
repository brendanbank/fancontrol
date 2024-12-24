from microdot import redirect
from microdot.helpers import wraps
from microdot.microdot import invoke_handler

def authorization_required(f):
    @wraps(f)
    async def wrapper(request, session, *args, **kwargs):
        print (session)
        return await invoke_handler(
            f, request, session, *args, **kwargs)
        
    return wrapper


