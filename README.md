# opensource-mini-project

Flask로 만든 간단한 방명록 웹페이지입니다.

## 실행 방법

```bash
pip install -r requirements.txt
python server.py
```

브라우저에서 http://localhost:8080 접속

## 구조

```
├── server.py          # Flask 서버
├── requirements.txt   # 의존성 목록
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

## 특징

- Flask 기반 웹 서버
- 방명록 데이터는 인메모리 리스트로 관리 (서버 재시작 시 초기화)
- Python 3.x 이상 필요
