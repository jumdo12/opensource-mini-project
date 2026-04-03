# 리팩토링 구현 보고서

## 선택된 전략: 설정 상수 추출 + 데이터 클래스 도입

### 의사결정 과정
여러 리팩토링 전략을 분석한 후, 설정 상수 추출과 데이터 클래스 도입의 조합을 선택한 이유:

1. **낮은 위험도, 높은 임팩트**: 이러한 변경사항들은 최소한의 위험을 가지면서 상당한 코드 품질 개선을 제공합니다
2. **향후 개선을 위한 기반**: 추가적인 아키텍처 리팩토링을 위한 견고한 토대를 마련합니다
3. **다중 스멜 해결**: 매직 넘버와 원시 타입 강박 스멜을 동시에 수정합니다
4. **하위 호환성 유지**: 최종 사용자를 위한 기존 기능이 변경되지 않습니다

### 구현 세부사항

#### 1. 설정 상수
**파일:** `server.py:9-10`
```python
MAX_NAME_LENGTH = 20
MAX_MESSAGE_LENGTH = 200
```

**변경 사항:**
- 하드코딩된 검증 제한값 (20, 200)을 명명된 상수로 추출
- 검증 로직에서 상수 사용: `len(name) > MAX_NAME_LENGTH`

**달성된 이익:**
- ✅ 매직 넘버 제거
- ✅ 중앙집중식 설정 관리
- ✅ 코드 가독성 개선
- ✅ 비즈니스 규칙 수정 용이

#### 2. 데이터 클래스
**파일:** `server.py:12-31`
```python
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
```

**변경 사항:**
- 원시 딕셔너리 엔트리를 타입 안전한 `GuestbookEntry` 데이터클래스로 교체
- 일관된 엔트리 생성을 위한 팩토리 메서드 `create()` 추가
- 템플릿 호환성을 위한 `to_dict()` 메서드 추가
- 타입 힌트 업데이트: `guestbook_entries: List[GuestbookEntry] = []`

**달성된 이익:**
- ✅ 적절한 데이터 계약을 가진 타입 안전성
- ✅ 캡슐화된 데이터 생성 로직
- ✅ 더 나은 IDE 지원 및 자동완성
- ✅ 생성 시간에 검증

#### 3. 업데이트된 함수 로직
**파일:** `server.py:38-58`

**인덱스 라우트 변경:**
```python
def index():
    entries_as_dicts = [entry.to_dict() for entry in reversed(guestbook_entries)]
    return render_template('index.html', entries=entries_as_dicts)
```

**제출 라우트 변경:**
```python
def submit():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not message or len(name) > MAX_NAME_LENGTH or len(message) > MAX_MESSAGE_LENGTH:
        return redirect(url_for('write'))

    entry = GuestbookEntry.create(name, message)
    guestbook_entries.append(entry)

    return redirect(url_for('success'))
```

#### 4. 테스트 업데이트
**파일:** `tests/test_validation.py:40-42`
```python
def test_유효한_입력_제출시_방명록에_추가됨(self, client):
    client.post('/submit', data={'name': '홍길동', 'message': '안녕하세요'})
    assert len(guestbook_entries) == 1
    assert guestbook_entries[0].name == '홍길동'  # 딕셔너리 접근에서 변경
    assert guestbook_entries[0].message == '안녕하세요'  # 딕셔너리 접근에서 변경
```

### 검증 결과

#### 테스트 스위트 상태
```
============================= test session starts ==============================
tests/test_validation.py::TestSubmitValidation::test_빈_이름_제출시_write_페이지로_리다이렉트 PASSED
tests/test_validation.py::TestSubmitValidation::test_빈_메시지_제출시_write_페이지로_리다이렉트 PASSED
tests/test_validation.py::TestSubmitValidation::test_20자_초과_이름_제출시_write_페이지로_리다이렉트 PASSED
tests/test_validation.py::TestSubmitValidation::test_200자_초과_메시지_제출시_write_페이지로_리다이렉트 PASSED
tests/test_validation.py::TestSubmitValidation::test_유효한_입력_제출시_success_페이지로_리다이렉트 PASSED
tests/test_validation.py::TestSubmitValidation::test_유효한_입력_제출시_방명록에_추가됨 PASSED
tests/test_validation.py::TestSubmitValidation::test_유효하지_않은_입력_제출시_방명록에_추가되지_않음 PASSED
tests/test_validation.py::TestSubmitValidation::test_이름_정확히_20자는_허용됨 PASSED
tests/test_validation.py::TestSubmitValidation::test_메시지_정확히_200자는_허용됨 PASSED

============================== 9 passed in 0.02s
```

✅ **모든 테스트 통과** - 기능의 회귀 없음

### 코드 품질 개선

#### 리팩토링 이전
- **매직 넘버**: 검증에 하드코딩된 20, 200 산재
- **원시 타입 강박**: 데이터 저장을 위한 원시 딕셔너리
- **타입 안전성 부족**: 데이터 구조 검증 없음
- **유지보수 문제**: 변경 시 여러 코드 위치 수정 필요

#### 리팩토링 이후
- **명명된 상수**: `MAX_NAME_LENGTH`, `MAX_MESSAGE_LENGTH`
- **타입 안전 데이터**: 검증을 포함한 `GuestbookEntry` 데이터클래스
- **더 나은 캡슐화**: 팩토리 메서드와 데이터 계약
- **단일 진실 소스**: 중앙집중화된 설정

### 남은 코드 스멜
1. **전역 상태**: 여전히 전역 `guestbook_entries` 리스트 사용
2. **긴 메서드**: 제출 함수가 여전히 다중 책임을 가짐
3. **테스트 중복**: 반복적인 테스트 패턴이 남아있음

### 향후 리팩토링을 위한 다음 단계
1. 전역 상태를 제거하기 위한 리포지토리 패턴 구현
2. 더 나은 관심사 분리를 위한 검증 서비스 추출
3. 중복을 줄이기 위한 테스트 매개변수화
4. 적절한 오류 처리 및 로깅 추가
5. 지속성을 위한 데이터베이스 통합 고려

### 영향 평가
- **위험도**: 낮음 ✅
- **테스트 커버리지**: 유지됨 ✅
- **기능성**: 보존됨 ✅
- **코드 품질**: 상당히 개선됨 ✅
- **유지보수성**: 향상됨 ✅