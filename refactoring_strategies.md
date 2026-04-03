# Refactoring Strategies for Identified Code Smells

## Strategy 1: Extract Configuration Constants
**Target Smell:** Magic Numbers
**Approach:** Extract hard-coded validation limits into named constants
**Benefits:**
- Centralized configuration management
- Improved readability
- Easy to modify business rules
- Better maintainability

**Implementation:**
```python
# Configuration constants
MAX_NAME_LENGTH = 20
MAX_MESSAGE_LENGTH = 200

# Usage in validation
if not name or not message or len(name) > MAX_NAME_LENGTH or len(message) > MAX_MESSAGE_LENGTH:
```

## Strategy 2: Introduce Data Classes
**Target Smell:** Primitive Obsession
**Approach:** Replace dictionary-based entries with proper data classes
**Benefits:**
- Type safety
- Encapsulated validation
- Clear data contracts
- Better IDE support

**Implementation:**
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

## Strategy 3: Repository Pattern for Data Management
**Target Smell:** Global State
**Approach:** Introduce a repository class to manage guestbook entries
**Benefits:**
- Eliminates global state
- Encapsulates data access logic
- Enables dependency injection for testing
- Thread-safe operations

**Implementation:**
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

## Strategy 4: Extract Validation Service
**Target Smell:** Long Method with Multiple Responsibilities
**Approach:** Separate validation logic into dedicated service
**Benefits:**
- Single Responsibility Principle
- Reusable validation logic
- Easier unit testing
- Clear separation of concerns

**Implementation:**
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

## Strategy 5: Test Parametrization
**Target Smell:** Duplicate Code in Tests
**Approach:** Use pytest parametrization to reduce test duplication
**Benefits:**
- Eliminates code duplication
- Easier to add new test cases
- More maintainable test suite
- Consistent test structure

**Implementation:**
```python
@pytest.mark.parametrize("name,message,expected_redirect", [
    ('', 'Hello', '/write'),  # Empty name
    ('John', '', '/write'),   # Empty message
    ('a' * 21, 'Hello', '/write'),  # Name too long
    ('John', 'a' * 201, '/write'),  # Message too long
    ('John', 'Hello', '/success'),  # Valid input
])
def test_submit_validation(client, name, message, expected_redirect):
    response = client.post('/submit', data={'name': name, 'message': message})
    assert response.status_code == 302
    assert expected_redirect in response.headers['Location']
```

## Recommended Implementation Order

### Phase 1: Foundation (Low Risk)
1. **Extract Configuration Constants** - Simple, no breaking changes
2. **Introduce Data Classes** - Gradual adoption possible

### Phase 2: Architecture (Medium Risk)
3. **Repository Pattern** - Requires careful testing
4. **Extract Validation Service** - Moderate refactoring

### Phase 3: Testing (Low Risk)
5. **Test Parametrization** - Improves test suite quality

## Selected Strategy: Extract Configuration Constants + Introduce Data Classes

**Reasoning:**
- Low risk, high impact combination
- Addresses multiple code smells simultaneously
- Provides foundation for future improvements
- Minimal breaking changes
- Easy to verify correctness

This approach will eliminate magic numbers and primitive obsession while laying groundwork for further architectural improvements.