import http.server
import socketserver
import os
import json

PORT = 5000
HOST = "0.0.0.0"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/token':
            token = os.environ.get('GITHUB_TOKEN', '')
            payload = json.dumps({'token': token}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            super().do_GET()

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("X-Frame-Options", "ALLOWALL")
        self.send_header("Content-Security-Policy", "frame-ancestors *")
        super().end_headers()

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    httpd.allow_reuse_address = True
    print(f"Serving on {HOST}:{PORT}")
    httpd.serve_forever()
