import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')

import logging
import uforms

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

from fancontrol import app
import os

from fancontrol.config import config

template_dir = 'fancontrol/templates/'

for fiel in os.listdir(template_dir):
    if fiel.endswith('.py'):
        log.debug(f'removed file {fiel}')
        os.remove(template_dir + fiel)
        
uforms.initialize(recompile=True)

app.run(port=5999,debug=True)	