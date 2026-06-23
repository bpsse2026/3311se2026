import http.server
import socketserver
import socket
import os
import json
import urllib.request
import urllib.error

PORT = 5000
HOST = "0.0.0.0"
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), 'progress-data.json')
JADWAL_FILE   = os.path.join(os.path.dirname(__file__), 'jadwal-events.json')

GH_REPO   = 'bpsse2026/3311se2026'
GH_BRANCH = 'main'

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/progress':
            try:
                with open(PROGRESS_FILE, 'r') as f:
                    data = f.read()
                payload = data.encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            except Exception as e:
                err = json.dumps({'ok': False, 'error': str(e)}).encode()
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(err)))
                self.end_headers()
                self.wfile.write(err)
        elif self.path == '/api/jadwal':
            try:
                with open(JADWAL_FILE, 'r') as f:
                    data = f.read()
                payload = data.encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            except Exception as e:
                err = json.dumps({'ok': False, 'error': str(e)}).encode()
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(err)))
                self.end_headers()
                self.wfile.write(err)
        elif self.path == '/api/has-token':
            has = bool(os.environ.get('GITHUB_TOKEN', '').strip())
            payload = json.dumps({'hasToken': has}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/progress':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)
                data = json.loads(body)
                pendataan      = max(0, min(100, int(data.get('pendataan', 0))))
                response       = max(0, min(100, int(data.get('response',  0))))
                formsSubmitted = max(0, int(data.get('formsSubmitted', 0)))
                payload_data = {'pendataan': pendataan, 'response': response, 'formsSubmitted': formsSubmitted}
                payload_str = json.dumps(payload_data, indent=2)
                with open(PROGRESS_FILE, 'w') as f:
                    f.write(payload_str)
                out = json.dumps({'ok': True}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(out)))
                self.end_headers()
                self.wfile.write(out)
            except Exception as e:
                err = json.dumps({'ok': False, 'error': str(e)}).encode()
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(err)))
                self.end_headers()
                self.wfile.write(err)

        elif self.path == '/api/jadwal':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)
                data = json.loads(body)
                payload_str = json.dumps(data, indent=2, ensure_ascii=False)
                with open(JADWAL_FILE, 'w', encoding='utf-8') as f:
                    f.write(payload_str)
                out = json.dumps({'ok': True}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(out)))
                self.end_headers()
                self.wfile.write(out)
            except Exception as e:
                err = json.dumps({'ok': False, 'error': str(e)}).encode()
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(err)))
                self.end_headers()
                self.wfile.write(err)

        elif self.path == '/api/github/push-jadwal':
            self._proxy_github_push(JADWAL_FILE, 'jadwal-events.json',
                                    'Update jadwal-events.json via admin panel')

        elif self.path == '/api/github/push-progress':
            self._proxy_github_push(PROGRESS_FILE, 'progress-data.json',
                                    'Update progress-data.json via admin panel')

        else:
            self.send_response(404)
            self.end_headers()

    def _proxy_github_push(self, local_file, gh_filename, commit_msg):
        token = os.environ.get('GITHUB_TOKEN', '').strip()
        if not token:
            err = json.dumps({'ok': False, 'error': 'GITHUB_TOKEN not configured on server'}).encode()
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(err)))
            self.end_headers()
            self.wfile.write(err)
            return
        try:
            length = int(self.headers.get('Content-Length', 0))
            body   = self.rfile.read(length)
            req_data = json.loads(body)
            sha    = req_data.get('sha', '')

            with open(local_file, 'r') as f:
                file_content = f.read()

            import base64
            content_b64 = base64.b64encode(file_content.encode('utf-8')).decode('ascii')

            api_url = f'https://api.github.com/repos/{GH_REPO}/contents/{gh_filename}'
            push_body = {
                'message': commit_msg,
                'content': content_b64,
                'branch': GH_BRANCH
            }
            if sha:
                push_body['sha'] = sha

            req = urllib.request.Request(
                api_url,
                data=json.dumps(push_body).encode('utf-8'),
                method='PUT',
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/vnd.github+json',
                    'X-GitHub-Api-Version': '2022-11-28',
                    'User-Agent': 'SEROJA-Admin'
                }
            )
            with urllib.request.urlopen(req) as resp:
                resp_body = resp.read()
                resp_json = json.loads(resp_body)
                new_sha   = resp_json.get('content', {}).get('sha', sha)
                out = json.dumps({'ok': True, 'sha': new_sha}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(out)))
                self.end_headers()
                self.wfile.write(out)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8', errors='replace')
            try:
                err_json = json.loads(err_body)
                detail = err_json.get('message', err_body)
            except Exception:
                detail = err_body
            err = json.dumps({'ok': False, 'error': f'HTTP {e.code}: {detail}'}).encode()
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(err)))
            self.end_headers()
            self.wfile.write(err)
        except Exception as e:
            err = json.dumps({'ok': False, 'error': str(e)}).encode()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(err)))
            self.end_headers()
            self.wfile.write(err)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("X-Frame-Options", "ALLOWALL")
        self.send_header("Content-Security-Policy", "frame-ancestors *")
        super().end_headers()

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            pass
        super().server_bind()

with ReusableTCPServer((HOST, PORT), Handler) as httpd:
    print(f"Serving on {HOST}:{PORT}")
    httpd.serve_forever()
