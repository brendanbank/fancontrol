import time
import sys
import asyncio
sys.path.append('/Users/brendan/src/fancontrol/lib')

from microdot import Microdot, send_file
from microdot.websocket import with_websocket

app = Microdot()


@app.route('/')
async def index(request):
    return send_file('index.html')


@app.route('/echo')
@with_websocket
async def echo(request, ws):
    i = 0
    while True:
        i += 1
        await ws.send(str(i))
        await asyncio.sleep(1)



app.run(debug=True, port = 5999)
