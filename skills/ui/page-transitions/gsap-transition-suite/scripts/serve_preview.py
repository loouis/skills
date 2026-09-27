#!/usr/bin/env python3
"""Serve this portable skill demo; optionally use a local GSAP file offline."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--port', type=int, default=4177)
parser.add_argument('--gsap', type=Path, help='Path to an existing gsap/dist/gsap.min.js')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
gsap_bytes = args.gsap.read_bytes() if args.gsap else None

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        route = self.path.split('?')[0]
        if gsap_bytes and route == '/vendor/gsap.min.js':
            data, mime = gsap_bytes, 'text/javascript'
        elif gsap_bytes and route in ('/demo/', '/demo/index.html'):
            data = (root / 'demo/index.html').read_bytes().replace(
                b'https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js', b'/vendor/gsap.min.js')
            mime = 'text/html'
        else:
            return super().do_GET()
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == '__main__':
    print(f'Preview: http://localhost:{args.port}/demo/', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(root))).serve_forever()
