from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from dataclasses import dataclass
from typing import List

app = Flask(__name__)

# Configuration constants
MAX_NAME_LENGTH = 20
MAX_MESSAGE_LENGTH = 200

@dataclass
class GuestbookEntry:
    name: str
    message: str
    date: str

    @classmethod
    def create(cls, name: str, message: str) -> 'GuestbookEntry':
        return cls(
            name=name.strip(),
            message=message.strip(),
            date=datetime.now().strftime('%Y-%m-%d %H:%M')
        )

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'message': self.message,
            'date': self.date
        }

guestbook_entries: List[GuestbookEntry] = []


@app.route('/')
@app.route('/home')
def index():
    entries_as_dicts = [entry.to_dict() for entry in reversed(guestbook_entries)]
    return render_template('index.html', entries=entries_as_dicts)


@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not message or len(name) > MAX_NAME_LENGTH or len(message) > MAX_MESSAGE_LENGTH:
        return redirect(url_for('write'))

    entry = GuestbookEntry.create(name, message)
    guestbook_entries.append(entry)

    return redirect(url_for('success'))


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    print('서버 실행 중 → http://localhost:8080')
    app.run(host='localhost', port=8080, debug=True)
