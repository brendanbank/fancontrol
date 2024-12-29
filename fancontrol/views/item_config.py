import logging
log = logging.getLogger(__name__)

from fancontrol.config import app, config
from fancontrol.views.login_view import authorization_required, admin_login
from microdot.utemplate import Template


@app.route('/config/<string:setting_name>', methods=['GET', 'POST'])
@authorization_required
async def setting_name(request, setting_name):

    item_clsobj = config.factory.get(setting_name)
    session = request.app._session.get(request)
    
    setting_obj = config.factory.get(setting_name)
    return setting_obj.process_form(session, request)