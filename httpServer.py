import sys
import time
import StringIO
import BaseHTTPServer
import httplib
from SimpleHTTPServer import SimpleHTTPRequestHandler

HandlerClass = SimpleHTTPRequestHandler
ServerClass  = BaseHTTPServer.HTTPServer

class simpleHandler(SimpleHTTPRequestHandler):

    def send_head(self,strReturn):
        if strReturn:
            f = StringIO.StringIO(strReturn)
            self.send_response(200)
            self.send_header("Content-type", 'text/plain')
            self.send_header("Content-Length", str(len(strReturn)))
            self.send_header("Last-Modified", time.localtime())
            self.end_headers()
            return f
        else:
            return None

    def do_GET(self):
        print self.path
        conn = httplib.HTTPConnection("shorturl.baiku.cn")
        conn.request("GET", self.path)
        rsp = conn.getresponse()
        print rsp.status, rsp.reason
        data = rsp.read()
        print data
        conn.close()
        time.sleep(3)
        f = self.send_head(data)
        if f:
            self.copyfile(f,self.wfile)
            f.close()

Protocol     = "HTTP/1.0"
if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 18980
server_address = ('127.0.0.1', port)
HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, simpleHandler)
sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()