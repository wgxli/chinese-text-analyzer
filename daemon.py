from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
import json

from colorama import Fore, Style
from g2pc import G2pC

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
        query = unquote(urlparse(self.path).geturl())[1:]
        print(f'[query] {Fore.BLUE}{query}{Style.RESET_ALL}')

        segments = [
            process_segment(segment)
            for segment in segmenter(query)
        ]
        response = json.dumps(segments)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.encode())

host, port = address = ('localhost', 1337)
daemon = HTTPServer(address, RequestHandler)
print(f'Web server initialized at {host}:{port}')
daemon.serve_forever()
