# Testing with PyUnit (unittest)

This project uses Python's built-in `unittest` framework (PyUnit) for testing. The tests are organized in the `tests` directory.

## Running Tests

You can run all tests using the test runner script:

```bash
python run_tests.py
```

Or run individual test files:

```bash
python -m unittest tests/test_app.py
python -m unittest tests/test_auth.py
```

You can also run specific test classes or methods:

```bash
python -m unittest tests.test_app.TestAppFunctions
python -m unittest tests.test_app.TestAppFunctions.test_hash_password
```

## Test Structure

The tests follow the Arrange-Act-Assert (AAA) pattern:

1. **Arrange**: Set up the test data and environment
2. **Act**: Perform the action being tested
3. **Assert**: Verify the results

## Mocking

For tests that involve external dependencies (like database connections), we use the `unittest.mock` module to create mock objects. This allows us to test the code in isolation.

Example:

```python
@patch('app.get_db_engine')
def test_user_exists(self, mock_get_db_engine):
    # Arrange - setup mocks
    mock_engine = MagicMock()
    mock_get_db_engine.return_value = mock_engine
    # ...

    # Act
    result = user_exists('testuser')

    # Assert
    self.assertTrue(result)
```

## Adding New Tests

To add new tests:

1. Create a new file in the `tests` directory with a name starting with `test_`
2. Import the `unittest` module and the functions you want to test
3. Create a class that inherits from `unittest.TestCase`
4. Add test methods that start with `test_`

## Code Coverage

To measure code coverage, you can install and use the `coverage` package:

```bash
pip install coverage
coverage run run_tests.py
coverage report
coverage html  # Generates an HTML report
```

This will show you how much of your code is covered by tests.

## Continuous Integration

Test automation is part of the CI/CD pipeline in this project. Tests are automatically run when code is pushed to the repository to ensure code quality.
