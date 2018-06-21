#!/usr/bin/python

import cgi
import logging
import re
import urllib
import urllib2
import urlparse

from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ForkingTCPServer

PORT = 8080

"""
HTTP Proxy class to redirect the obsolete netlist URL for
the CallWall program by NullRiver,
     http://www.nullriver.com/products/callwall
"""
class Proxy(SimpleHTTPRequestHandler):

    def do_netlist (self):
        """
        Process the CallWall netlist URL
        :return: True if CallWall netlist URL was detected and processed.
                 False if not.
        """
        url = urlparse.urlparse(self.path)

        if url.scheme != 'http' or \
            url.netloc != 'www.whocalled.us' or \
            url.path != '/do':
            return False

        query = cgi.parse_qs(url.query)
        if query.get('action') != ['getScore'] or \
            query.get('name') != ['callwall'] or \
            query.get('pass') != ['callwall']:
            return False

        phoneNumbers = query.get('phoneNumber')
        if not phoneNumbers or len(phoneNumbers) != 1:
            return False

        request = 'https://www.nomorobo.com/lookup/%s' % (phoneNumbers[0])

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

        return True

    def do_GET(self):
        """
        Process the HTTP GET Request
        """

        logging.debug('Processing %s', self.path)

        if not self.do_netlist():
            self.copyfile(urllib.urlopen(self.path, proxies={}), self.wfile)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])

    httpd = ForkingTCPServer(('', PORT), Proxy)
    logging.info('Listening at port: %d', PORT)
    httpd.serve_forever()
