from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from datetime import datetime
from html import escape

# 방명록 인메모리 저장소
guestbook_entries = []


class GuestbookHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urlparse(self.path).path

        if path in ('/', '/index.html'):
            self.serve_index()
        elif path == '/write.html':
            self.serve_file('write.html')
        elif path == '/success.html':
            self.serve_file('success.html')
        else:
            self.send_error(404, '페이지를 찾을 수 없습니다.')

    def do_POST(self):
        if self.path == '/submit':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            params = parse_qs(body)

            name = params.get('name', [''])[0].strip()
            message = params.get('message', [''])[0].strip()

            if name and message:
                guestbook_entries.append({
                    'name': escape(name),
                    'message': escape(message),
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                })

            self.send_response(302)
            self.send_header('Location', '/success.html')
            self.end_headers()
        else:
            self.send_error(404)

    def serve_index(self):
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            content = f.read()

        if guestbook_entries:
            entries_html = ''.join(
                f'''
                <div class="entry">
                    <div class="entry-header">
                        <span class="entry-name">{e["name"]}</span>
                        <span class="entry-date">{e["date"]}</span>
                    </div>
                    <p class="entry-message">{e["message"]}</p>
                </div>'''
                for e in reversed(guestbook_entries)
            )
        else:
            entries_html = '<p class="empty">아직 방명록이 없습니다. 첫 번째로 남겨보세요!</p>'

        content = content.replace('{{entries}}', entries_html)
        self._respond(content)

    def serve_file(self, filename):
        with open(f'templates/{filename}', 'r', encoding='utf-8') as f:
            content = f.read()
        self._respond(content)

    def _respond(self, content):
        encoded = content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):
        print(f'[{self.log_date_time_string()}] {format % args}')


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), GuestbookHandler)
    print('서버 실행 중 → http://localhost:8080')
    server.serve_forever()
