# Repository Guidance

## Tests

- Use Python's built-in `unittest`; do not use pytest.
- Initialize the venv if needed.
- Run the full suite with `.venv/bin/python -m unittest discover -s tests`.
- Run a focused test with `.venv/bin/python -m unittest tests.test_demo.DemoTestCase.test_case`.
- Prefer not to create a new file for new tests cases. Instead, add the cases to a relevant existing file if one exists.
