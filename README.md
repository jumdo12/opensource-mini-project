# opensource-mini-project

Flask로 만든 간단한 방명록 웹페이지입니다.

## 실행 방법

```bash
pip install -r requirements.txt
python server.py
```

브라우저에서 http://localhost:8080 접속

## 테스트 실행

```bash
python -m pytest tests/ -v
```

## 구조

```
├── server.py          # Flask 서버
├── requirements.txt   # 의존성 목록
├── conftest.py        # pytest 픽스처
├── tests/
│   └── test_validation.py  # 입력 유효성 검사 테스트
└── templates/
    ├── index.html     # 방명록 목록
    ├── write.html     # 글쓰기
    └── success.html   # 등록 완료
```

## 엔드포인트

| 경로 | 설명 |
|------|------|
| `/` | 방명록 목록 |
| `/home` | 방명록 목록 (동일) |
| `/write` | 글쓰기 페이지 |
| `/submit` | 글 등록 (POST) |
| `/success` | 등록 완료 페이지 |

## 유효성 검사

글 등록 시 아래 조건을 충족하지 않으면 `/write`로 리다이렉트됩니다.

| 필드 | 조건 |
|------|------|
| 이름 | 필수, 최대 20자 |
| 메시지 | 필수, 최대 200자 |

## 특징

- Flask 기반 웹 서버
- pytest + pytest-flask 기반 TDD 테스트 환경
- 방명록 데이터는 인메모리 리스트로 관리 (서버 재시작 시 초기화)
- Python 3.x 이상 필요
