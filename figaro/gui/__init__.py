"""Serves the compiled React frontend locally for the GUI"""

import http.server, socketserver, threading, os
from typing import Tuple, Optional

from figaro import params

"""The actual HTTP daemon"""
httpd: socketserver.TCPServer = None
"""The path to the GUI package directory"""
bpath: str = os.path.join(params.BPATH, 'figaro', 'gui')

class FigaroHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super(FigaroHandler, self).__init__(request, client_address, server, directory=os.path.join(bpath, params.GUI_PATH))

    def log_message(self, format, *args):
        return

def _start():
    """The function that will actually start the server"""
    global httpd
    httpd = socketserver.TCPServer((params.GUI_HOST, params.GUI_PORT), FigaroHandler)
    # print(f'Server listening on {params.GUI_HOST}:{params.GUI_PORT} ... ')
    httpd.serve_forever()

def start():
    """Start the server hosting the static files"""
    threading.Thread(target=_start).start()

def stop():
    """Stops the server hosting the static files"""
    httpd.shutdown()