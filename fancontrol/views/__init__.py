from fancontrol.config import app
from microdot.session import Session, with_session

from fancontrol.views.login_view import authorization_required, admin_login

import fancontrol.views.index
