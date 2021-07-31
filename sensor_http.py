"""
Very simple HTTP server in python.
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from multiprocessing import Queue
import time

class QueuingHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, sonos_queue, light_queue, lux_queue, bind_and_activate=True):
        HTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.sonos_queue = sonos_queue
        self.light_queue = light_queue
        self.lux_queue = lux_queue

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #print self.path
        if (self.path == "/light_toggle"):
          print "Light Requested"
          self.server.light_queue.put("Toggle");
        if (self.path.startswith('/brightness/')):
          self.server.lux_queue.put(int(self.path[12:]))
        self._set_headers()
        self.wfile.write("Request Processed\n")
        
def run(sonos_queue,light_queue,lux_queue,server_class=QueuingHTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class, sonos_queue,light_queue,lux_queue)
    print 'Starting httpd...'
    httpd.serve_forever()
      
