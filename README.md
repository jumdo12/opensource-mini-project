# opensource-mini-project

Flask로 만든 간단한 방명록 웹 애플리케이션입니다.
TDD(Test-Driven Development) 방식으로 개발되었으며, Swagger UI를 통한 API 문서와 Sphinx 기반 기술 문서를 제공합니다.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.3-lightgrey?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 주요 기능

- 방명록 글 목록 조회 (최신순 정렬)
- 이름 + 메시지 작성 및 제출
- 입력 유효성 검사 (이름 최대 20자, 메시지 최대 200자)
- **Swagger UI** (`/apidocs`): API를 브라우저에서 직접 테스트
- **Sphinx 문서** (GitHub Pages): 코드 docstring 기반 기술 문서

---

## 문서

| 문서 | URL |
|------|-----|
| Sphinx 기술 문서 | GitHub Pages (아래 설정 참고) |
| Swagger UI | 서버 실행 후 http://localhost:8080/apidocs |

### GitHub Pages 설정 방법

1. GitHub 저장소 → **Settings** → **Pages**
2. Source: **GitHub Actions** 선택
3. `main` 브랜치에 push하면 자동 빌드 및 배포

---

## 빠른 시작

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 서버 실행

```bash
python run.py
```

브라우저에서 http://localhost:8080 접속

### 3. Swagger UI 확인

```
http://localhost:8080/apidocs
```

### 4. Sphinx 문서 로컬 빌드

```bash
sphinx-build -b html docs docs/_build/html
open docs/_build/html/index.html
```

---

## 테스트 실행

```bash
python -m pytest tests/ -v
```

---

## 프로젝트 구조

```
├── run.py                 # 실행 진입점
├── requirements.txt       # 의존성 목록
├── conftest.py            # pytest 픽스처
├── app/
│   ├── __init__.py
│   ├── server.py          # Flask 서버 (라우팅 + 유효성 검사)
│   └── templates/
│       ├── index.html     # 방명록 목록 페이지
│       ├── write.html     # 글쓰기 페이지
│       └── success.html   # 등록 완료 페이지
├── tests/
│   └── test_validation.py # 입력 유효성 검사 테스트 (TDD)
├── docs/
│   ├── conf.py            # Sphinx 설정
│   ├── index.rst          # 문서 목차
│   └── server.rst         # server 모듈 자동 문서화
└── .github/
    └── workflows/
        └── docs.yml       # GitHub Pages 자동 배포 워크플로
```

---

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 방명록 목록 |
| GET | `/home` | 방명록 목록 (동일) |
| GET | `/write` | 글쓰기 페이지 |
| POST | `/submit` | 글 등록 |
| GET | `/success` | 등록 완료 페이지 |
| GET | `/apidocs` | Swagger UI |

---

## 유효성 검사

글 등록 시 아래 조건을 충족하지 않으면 `/write`로 리다이렉트됩니다.

| 필드 | 조건 |
|------|------|
| 이름 | 필수, 최대 20자 |
| 메시지 | 필수, 최대 200자 |

---

## 기술 스택

| 항목 | 내용 |
|------|------|
| 언어 | Python 3.x |
| 웹 프레임워크 | Flask 3.1.3 |
| API 문서 | Flasgger (Swagger UI) |
| 기술 문서 | Sphinx + sphinx-rtd-theme |
| 테스트 | pytest + pytest-flask |
| CI/CD | GitHub Actions |
