from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

guestbook_entries = []


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', entries=list(reversed(guestbook_entries)))


@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if name and message:
        guestbook_entries.append({
            'name': name,
            'message': message,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        })

    return redirect(url_for('success'))


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    print('서버 실행 중 → http://localhost:8080')
    app.run(host='localhost', port=8080, debug=True)
