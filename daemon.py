#! /bin/python3
# daemon.py - Local HTTP daemon for Chinese text segmentation.
# Note that there is no error validation.
# I wouldn't run this on a public-facing webserver.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
import json

from g2pc import G2pC

# Use G2pC for Chinese segmentation
segmenter = G2pC()


def process_segment(segment):
    char, pos, pinyin, _, meaning, _ = segment
    return {
        'character': char,
        'pos': pos,
        'pinyin': pinyin.split(),
        'meaning': meaning[1:-1].split('/'),
    }


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get the query text.
        query = unquote(urlparse(self.path).geturl())[1:]
        print('[query]', query)

        segments = [
            process_segment(segment)
            for segment in segmenter(query)
        ]
        response = json.dumps(segments)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.encode())


# Address for the local server
host, port = address = ('localhost', 1337)

daemon = HTTPServer(address, RequestHandler)
print(f'Web server initialized at {host}:{port}')
daemon.serve_forever()
