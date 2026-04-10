"""애플리케이션 실행 진입점."""

from app.server import app

if __name__ == '__main__':
    print('서버 실행 중 → http://localhost:8080')
    app.run(host='localhost', port=8080, debug=True)
