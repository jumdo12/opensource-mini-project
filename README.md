# opensource-mini-project

순수 파이썬과 HTML만으로 만든 간단한 방명록 웹페이지입니다.

## 실행 방법

```bash
python server.py
```

브라우저에서 http://localhost:8080 접속

## 구조

```
├── server.py          # HTTP 서버
└── templates/
    ├── index.html     # 방명록 목록
    ├── write.html     # 글쓰기
    └── success.html   # 등록 완료
```

## 특징

- 외부 라이브러리 없음 (표준 라이브러리만 사용)
- 방명록 데이터는 인메모리 리스트로 관리 (서버 재시작 시 초기화)
- Python 3.x 이상 필요
