# Code Smells Analysis

## Identified Code Smells

### 1. **Global State (Data Clump)**
- **Location:** `server.py:6`
- **Code:** `guestbook_entries = []`
- **Description:** Using a global list to store application data
- **Why it's a smell:**
  - Makes code harder to test, debug, and scale
  - Creates hidden dependencies between functions
  - Makes the application non-thread-safe
  - Data is lost when server restarts
  - Violates encapsulation principles

### 2. **Magic Numbers**
- **Location:** `server.py:25`
- **Code:** `len(name) > 20 or len(message) > 200`
- **Description:** Hard-coded validation limits scattered in code
- **Why it's a smell:**
  - Makes business rules difficult to maintain and modify
  - If requirements change, need to hunt down all occurrences
  - No central place to manage configuration
  - Reduces code readability and maintainability

### 3. **Long Method with Multiple Responsibilities**
- **Location:** `server.py:21-34` (submit function)
- **Code:** 14-line function handling validation, processing, and response
- **Description:** The submit function handles form validation, data processing, and response logic
- **Why it's a smell:**
  - Violates Single Responsibility Principle
  - Makes the function harder to test individual aspects
  - Difficult to understand and modify
  - Changes to validation logic require touching data storage logic

### 4. **Primitive Obsession**
- **Location:** `server.py:28-32`
- **Code:** Using raw dictionaries for guestbook entries
- **Description:** Using primitive data structures instead of proper domain objects
- **Why it's a smell:**
  - No type safety or validation
  - No encapsulation of behavior
  - Easy to make mistakes with key names
  - No clear interface or contract for data structure

### 5. **Duplicate Code in Tests**
- **Location:** `tests/test_validation.py:13-56`
- **Code:** Repetitive test structure with similar assertions
- **Description:** Multiple tests with nearly identical setup and assertion patterns
- **Why it's a smell:**
  - Code duplication makes tests harder to maintain
  - When assertion logic changes, multiple tests need updating
  - Inconsistent language use (Korean test names, English code)
  - Violates DRY (Don't Repeat Yourself) principle

## Impact Assessment
These smells collectively make the codebase:
- Harder to maintain and extend
- More prone to bugs
- Difficult to test comprehensively
- Less readable and understandable
- Not suitable for production environments