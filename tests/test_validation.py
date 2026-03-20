"""
입력 유효성 검사 TDD 테스트
- 이름: 필수, 최대 20자
- 메시지: 필수, 최대 200자
- 유효하지 않으면 /write 로 리다이렉트
- 유효하면 /success 로 리다이렉트 + 방명록에 추가
"""
from server import guestbook_entries


class TestSubmitValidation:

    def test_빈_이름_제출시_write_페이지로_리다이렉트(self, client):
        response = client.post('/submit', data={'name': '', 'message': '안녕하세요'})
        assert response.status_code == 302
        assert '/write' in response.headers['Location']

    def test_빈_메시지_제출시_write_페이지로_리다이렉트(self, client):
        response = client.post('/submit', data={'name': '홍길동', 'message': ''})
        assert response.status_code == 302
        assert '/write' in response.headers['Location']

    def test_20자_초과_이름_제출시_write_페이지로_리다이렉트(self, client):
        response = client.post('/submit', data={'name': '가' * 21, 'message': '안녕하세요'})
        assert response.status_code == 302
        assert '/write' in response.headers['Location']

    def test_200자_초과_메시지_제출시_write_페이지로_리다이렉트(self, client):
        response = client.post('/submit', data={'name': '홍길동', 'message': '가' * 201})
        assert response.status_code == 302
        assert '/write' in response.headers['Location']

    def test_유효한_입력_제출시_success_페이지로_리다이렉트(self, client):
        response = client.post('/submit', data={'name': '홍길동', 'message': '안녕하세요'})
        assert response.status_code == 302
        assert '/success' in response.headers['Location']

    def test_유효한_입력_제출시_방명록에_추가됨(self, client):
        client.post('/submit', data={'name': '홍길동', 'message': '안녕하세요'})
        assert len(guestbook_entries) == 1
        assert guestbook_entries[0]['name'] == '홍길동'
        assert guestbook_entries[0]['message'] == '안녕하세요'

    def test_유효하지_않은_입력_제출시_방명록에_추가되지_않음(self, client):
        client.post('/submit', data={'name': '', 'message': '안녕하세요'})
        assert len(guestbook_entries) == 0

    def test_이름_정확히_20자는_허용됨(self, client):
        response = client.post('/submit', data={'name': '가' * 20, 'message': '안녕하세요'})
        assert response.status_code == 302
        assert '/success' in response.headers['Location']

    def test_메시지_정확히_200자는_허용됨(self, client):
        response = client.post('/submit', data={'name': '홍길동', 'message': '가' * 200})
        assert response.status_code == 302
        assert '/success' in response.headers['Location']
