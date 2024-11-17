# Chat Application with Test-Driven Development

This project demonstrates advanced testing practices including Test-Driven Development (TDD), unit testing, and integration testing using pytest. While it implements a basic chat application, the main focus is on showcasing various testing methodologies and best practices.

## 🎯 Key Testing Features

- **Test-Driven Development (TDD)** approach demonstrated in `color_test.py`
- **Unit Testing** with mock objects and fixtures
- **Integration Testing** for multi-client scenarios
- **Comprehensive Test Coverage** across different components
- **Mock Objects** and dependency injection
- **Pytest Fixtures** for test setup and teardown
- **Error Handling Tests** for robustness

## 🧪 Test Structure

### Unit Tests

1. **Color Selection Tests** (`color_test.py`):
   - Validates color selection functionality
   - Demonstrates TDD principles
   - Tests edge cases and error handling
   - Uses mock inputs for consistent testing

2. **Message Handling Tests** (`handle_test.py`):
   - Tests message processing functionality
   - Uses mock objects for network operations
   - Covers success and failure scenarios
   - Validates broadcast functionality

3. **Client Removal Tests** (`remove_test.py`):
   - Tests client disconnection handling
   - Validates cleanup operations
   - Ensures proper resource management
   - Tests edge cases with invalid clients

### Integration Tests (`integration_test.py`)

- Tests multiple client interactions
- Validates message distribution
- Tests simultaneous messaging
- Handles unexpected disconnections
- Uses threading for realistic scenarios

## 🚀 Running the Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest color_test.py
pytest handle_test.py
pytest remove_test.py
pytest integration_test.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=.
```
## 🛠️ Testing Tools & Techniques Used

### Pytest Features
- Fixtures for test setup
- Mock objects and patches
- Exception testing

### Mock Objects
- Socket mocking
- Input/Output mocking
- Function mocking
- Network operation simulation

### Testing Patterns
- Arrange-Act-Assert pattern
- Test isolation
