"""
방명록 Flask 서버 모듈.

이 모듈은 방명록 웹 애플리케이션의 라우팅과 비즈니스 로직을 담당합니다.
사용자는 방명록 목록 조회, 글 작성, 제출을 할 수 있습니다.
"""

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from dataclasses import dataclass
from typing import List
from flasgger import Swagger

app = Flask(__name__, template_folder='templates')
swagger = Swagger(app)

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
    """방명록 목록 페이지를 반환합니다.

    등록된 방명록 항목들을 최신순으로 보여주는 HTML 페이지를 렌더링합니다.

    Returns:
        str: 방명록 목록이 포함된 HTML 응답.
    """
    entries_as_dicts = [entry.to_dict() for entry in reversed(guestbook_entries)]
    return render_template('index.html', entries=entries_as_dicts)


@app.route('/write')
def write():
    """방명록 글쓰기 페이지를 반환합니다.

    사용자가 이름과 메시지를 입력할 수 있는 폼 페이지를 렌더링합니다.

    Returns:
        str: 글쓰기 폼이 포함된 HTML 응답.
    """
    return render_template('write.html')


@app.route('/submit', methods=['POST'])
def submit():
    """방명록 글을 제출합니다.

    POST 요청으로 전달된 이름과 메시지를 검증한 후 방명록에 추가합니다.

    Form Parameters:
        name (str): 작성자 이름. 필수, 최대 20자.
        message (str): 남길 메시지. 필수, 최대 200자.

    Returns:
        Response: 유효한 경우 /success로, 유효하지 않은 경우 /write로 리다이렉트.

    ---
    tags:
      - Guestbook
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: 작성자 이름 (최대 20자)
        maxLength: 20
      - name: message
        in: formData
        type: string
        required: true
        description: 방명록 메시지 (최대 200자)
        maxLength: 200
    responses:
      302:
        description: |
          유효한 입력이면 /success로,
          유효하지 않은 입력이면 /write로 리다이렉트.
    """
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not message or len(name) > MAX_NAME_LENGTH or len(message) > MAX_MESSAGE_LENGTH:
        return redirect(url_for('write'))

    entry = GuestbookEntry.create(name, message)
    guestbook_entries.append(entry)

    return redirect(url_for('success'))


@app.route('/success')
def success():
    """방명록 등록 완료 페이지를 반환합니다.

    글이 성공적으로 등록된 후 보여주는 완료 페이지를 렌더링합니다.

    Returns:
        str: 등록 완료 메시지가 포함된 HTML 응답.
    """
    return render_template('success.html')
