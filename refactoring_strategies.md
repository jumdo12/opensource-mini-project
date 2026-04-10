# 코드 스멜 리팩토링 전략

## 전략 1: 설정 상수 추출
**대상 스멜:** 매직 넘버
**접근법:** 하드코딩된 검증 제한값들을 명명된 상수로 추출
**장점:**
- 중앙집중식 설정 관리
- 가독성 향상
- 비즈니스 규칙 수정 용이
- 유지보수성 향상

**구현 예시:**
```python
# 설정 상수
MAX_NAME_LENGTH = 20
MAX_MESSAGE_LENGTH = 200

# 검증에서 사용
if not name or not message or len(name) > MAX_NAME_LENGTH or len(message) > MAX_MESSAGE_LENGTH:
```

## 전략 2: 데이터 클래스 도입
**대상 스멜:** 원시 타입 강박
**접근법:** 딕셔너리 기반 엔트리를 적절한 데이터 클래스로 교체
**장점:**
- 타입 안전성
- 캡슐화된 검증
- 명확한 데이터 계약
- 더 나은 IDE 지원

**구현 예시:**
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GuestbookEntry:
    name: str
    message: str
    date: str

    @classmethod
    def create(cls, name: str, message: str):
        return cls(
            name=name.strip(),
            message=message.strip(),
            date=datetime.now().strftime('%Y-%m-%d %H:%M')
        )
```

## 전략 3: 데이터 관리용 리포지토리 패턴
**대상 스멜:** 전역 상태
**접근법:** 방명록 엔트리 관리를 위한 리포지토리 클래스 도입
**장점:**
- 전역 상태 제거
- 데이터 접근 로직 캡슐화
- 테스트를 위한 의존성 주입 가능
- 스레드 안전 연산

**구현 예시:**
```python
class GuestbookRepository:
    def __init__(self):
        self._entries = []

    def add_entry(self, entry: GuestbookEntry):
        self._entries.append(entry)

    def get_all_entries(self):
        return list(reversed(self._entries))

    def clear(self):
        self._entries.clear()
```

## 전략 4: 검증 서비스 추출
**대상 스멜:** 다중 책임을 가진 긴 메서드
**접근법:** 검증 로직을 전용 서비스로 분리
**장점:**
- 단일 책임 원칙
- 재사용 가능한 검증 로직
- 단위 테스트 용이
- 관심사의 명확한 분리

**구현 예시:**
```python
class ValidationService:
    @staticmethod
    def validate_entry(name: str, message: str) -> bool:
        name = name.strip() if name else ''
        message = message.strip() if message else ''

        if not name or not message:
            return False

        if len(name) > MAX_NAME_LENGTH or len(message) > MAX_MESSAGE_LENGTH:
            return False

        return True
```

## 전략 5: 테스트 매개변수화
**대상 스멜:** 테스트 코드 중복
**접근법:** pytest 매개변수화를 사용하여 테스트 중복 감소
**장점:**
- 코드 중복 제거
- 새로운 테스트 케이스 추가 용이
- 더 유지보수하기 쉬운 테스트 스위트
- 일관된 테스트 구조

**구현 예시:**
```python
@pytest.mark.parametrize("name,message,expected_redirect", [
    ('', 'Hello', '/write'),  # 빈 이름
    ('John', '', '/write'),   # 빈 메시지
    ('a' * 21, 'Hello', '/write'),  # 이름이 너무 긴 경우
    ('John', 'a' * 201, '/write'),  # 메시지가 너무 긴 경우
    ('John', 'Hello', '/success'),  # 유효한 입력
])
def test_submit_validation(client, name, message, expected_redirect):
    response = client.post('/submit', data={'name': name, 'message': message})
    assert response.status_code == 302
    assert expected_redirect in response.headers['Location']
```

## 권장 구현 순서

### 1단계: 기초 (낮은 위험도)
1. **설정 상수 추출** - 단순하며 깨트리는 변경 사항 없음
2. **데이터 클래스 도입** - 점진적 적용 가능

### 2단계: 아키텍처 (중간 위험도)
3. **리포지토리 패턴** - 신중한 테스트 필요
4. **검증 서비스 추출** - 중간 정도의 리팩토링

### 3단계: 테스트 (낮은 위험도)
5. **테스트 매개변수화** - 테스트 스위트 품질 개선

## 선택된 전략: 설정 상수 추출 + 데이터 클래스 도입

**선택 이유:**
- 낮은 위험도, 높은 임팩트의 조합
- 여러 코드 스멜을 동시에 해결
- 향후 개선을 위한 기반 제공
- 최소한의 깨트리는 변경사항
- 정확성 검증 용이

이 접근법은 매직 넘버와 원시 타입 강박을 제거하면서 향후 아키텍처 개선을 위한 기반을 마련합니다.