#!/usr/bin/python
# HTTP Proxy for the CallWall program by NullRiver,
#     http://www.nullriver.com/products/callwall
# Changes Netlist to use NomoRobo instead.
#

import SocketServer
import SimpleHTTPServer
import re
import urllib
import urllib2
import urlparse
import StringIO

PORT = 8080

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = urlparse.urlparse(self.path)
        if url.netloc == 'www.whocalled.us':
            request = 'https://www.nomorobo.com/lookup/%s' % (url.query[url.query.rfind('=')+1:],)

            try:
                response = urllib2.urlopen(request)

                match = re.findall('(?i)do not answer', response.read())
                if match:
                    score=11
                else:
                    score=6

            except urllib2.HTTPError, e:
                score=0

            print '%s -> %s' % (request, score)
            self.copyfile(StringIO.StringIO('success=1&score=%d' % (score,)), self.wfile)

        else:
            self.copyfile(urllib.urlopen(self.path), self.wfile)

if __name__ == '__main__':
    httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
    print 'Listening at port: %d' % (PORT,)
    httpd.serve_forever()
