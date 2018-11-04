"""
Very simple HTTP server in python.
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from multiprocessing import Queue
import time

class QueuingHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, queue, bind_and_activate=True):
        HTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.data_queue = queue

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print self.path
        if (self.path == "/heaton"):
          print "Heat On"
          time.sleep(5)
          self.server.data_queue.put(1);
        if (self.path == "/heatoff"):
          print "Heat Off"
          self.server.data_queue.put(0);
        if (self.path == "/windowopen"):
          print "Window Open"
          self.server.data_queue.put(3);
        if (self.path == "/windowclosed"):
          print "Window Closed"
          self.server.data_queue.put(2);          
        self._set_headers()
        self.wfile.write("Processed\n")
        
def run(out_queue,server_class=QueuingHTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class, out_queue)
    print 'Starting httpd...'
    httpd.serve_forever()
      
