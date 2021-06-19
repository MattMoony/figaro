"""Serves the compiled React frontend locally for the GUI"""

import http.server, socketserver, threading, os, json
from typing import Tuple, Optional

from lib import utils, params

"""The actual HTTP daemon"""
httpd: socketserver.TCPServer = None
"""The path to the GUI package directory"""
bpath: str = os.path.join(params.BPATH, 'lib', 'gui')
"""The config for the HTTP server"""
conf: object = {}

class FigaroHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super(FigaroHandler, self).__init__(request, client_address, server, directory=os.path.join(bpath, 'web', 'public'))

    def log_message(self, format, *args):
        return

def _start():
    """The function that will actually start the server"""
    global httpd
    httpd = socketserver.TCPServer((conf['host'], conf['port']), FigaroHandler)
    # print(f'Server listening on {params.GUI_HOST}:{params.GUI_PORT} ... ')
    httpd.serve_forever()

def start():
    """Start the server hosting the static files"""
    global conf
    cpath = os.path.join(bpath, 'dist', 'config', 'conf.json')
    if not os.path.isfile(cpath):
        utils.printwrn(f'Config file ("{cpath}") missing ... trying to (re)compile GUI ... ')
        os.system(f'cd {bpath} && npm run build')
    if not os.path.isfile(cpath):
        utils.printerr(f'Config file "{cpath}" doesn\'t exist ... ')
        os._exit(1)
    with open(cpath, 'r') as f:
        conf = json.load(f)
    threading.Thread(target=_start).start()

def stop():
    """Stops the server hosting the static files"""
    if httpd:
        httpd.shutdown()