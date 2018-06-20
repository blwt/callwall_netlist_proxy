#!/usr/bin/python
#
# HTTP Proxy to update the netlist URL for the CallWall program by NullRiver,
#     http://www.nullriver.com/products/callwall
#

import logging
import re
import urllib2
import urlparse

from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ForkingTCPServer

PORT = 8080

class Proxy(SimpleHTTPRequestHandler):

    def do_GET(self):

        logging.debug('Processing %s', self.path)
        url = urlparse.urlparse(self.path)

        if url.netloc == 'www.whocalled.us':
            request = 'https://www.nomorobo.com/lookup/%s' % (url.query[url.query.rfind('=')+1:],)

            try:
                response = urllib2.urlopen(request)
                html_response = response.read()

                match = re.findall('(?i)do not answer', html_response)
                if match:
                    score=11
                else:
                    score=6

            except urllib2.HTTPError, e:
                score=0

            logging.info('%s -> %s', request, score)
            self.wfile.write('success=1&score=%d' % (score,))

        else:
            try:
                self.copyfile(urllib2.urlopen(self.path), self.wfile)                
            except urllib2.HTTPError, e:
                self.send_response(e.code)
            except urllib2.URLError, e:
                self.send_response(404)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])

    # Turn off proxy
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

    httpd = ForkingTCPServer(('', PORT), Proxy)
    logging.info('Listening at port: %d', PORT)
    httpd.serve_forever()
