#!/usr/bin/python

import cgi
import logging
import re
import urllib
import urllib2
import urlparse

from optparse import OptionParser
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ForkingTCPServer

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

    parser = OptionParser()
    parser.add_option('-p', '--port', type='int', help='Listening port number', default=8080)
    parser.add_option('-v', '--verbose', type='choice', action='store',
        choices=[k.lower() for k in logging._levelNames.keys() if isinstance(k, basestring)],
        default=logging.getLevelName(logging.INFO).lower(),
        help='Set the verbosity of the log level')
    options, args = parser.parse_args()

    logging.basicConfig(
        level=logging.getLevelName(options.verbose.upper()),
        handlers=[logging.StreamHandler()])

    httpd = ForkingTCPServer(('', options.port), Proxy)
    logging.info('Listening at port: %d', options.port)
    httpd.serve_forever()
