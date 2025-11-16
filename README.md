# HackerNews API Test — Local setup & running tests

This document explains how this framework can be set up locally and run the test-suite on macOS (zsh). Adjust the commands appropriately for other shells.

## Prerequisites

- Python 3.9+ installed. (This project was developed with Python 3.9.6.)
- Git
- (Optional recommended) pyenv for managing Python versions

## Quick overview

- Create a virtual environment at `.venv`.
- Install dependencies from `requirements.txt`.
- Run tests with `pytest` (we include `pytest-html` for HTML reports).

## Clone the repository

```bash
git clone <repo-url> hackernews-api-test
cd hackernews-api-test
```

Replace `<repo-url>` with your repository HTTP/SSH URL.

## Create and activate a virtual environment (recommended)

This project expects a local virtual environment at `.venv`. On macOS (zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If you prefer not to activate the venv, you can still run the bundled Python directly with `./.venv/bin/python`.

## Upgrade pip and install dependencies

With the venv activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Or, without activating:

```bash
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
```

If you encounter permission or platform issues, ensure the venv was created with the same Python binary you intend to use.

## Environment variables / .env

This project may read configuration from environment variables via `python-dotenv` (see `core/config.py`). Create a `.env` file at the project root if you need to supply local values. Example `.env`:

```env
# Example values — adjust for your environment
BASE_URL=https://hacker-news.firebaseio.com/v0/
# any other keys used by core/config.py
```

After creating `.env`, the code normally calls `load_dotenv()` (or similar) to pick up these values. If a helper to load the env isn't present, ensure the runtime loads the `.env` before running tests.

## Running tests

Run the full test-suite (from project root):

```bash
pytest -v
```

Generate a HTML report (requires `pytest-html` in `requirements.txt`):

```bash
pytest -v --html=report.html
# open with your browser
open report.html
```

Run a single test file or test function:

```bash
pytest -q tests/test_top_stories.py
# or a specific test
pytest tests/test_top_stories.py::test_some_behavior -q
```

Run tests without activating the venv (using the venv python):

```bash
./.venv/bin/python -m pytest -v
```

Note for macOS Terminal
-----------------------

When running tests from the macOS Terminal, always run pytest from the project root and prefer using the venv's Python to avoid import issues (for example, the "No module named 'core'" error). Either activate the venv first:

```bash
source .venv/bin/activate
pytest -v
```

or run pytest directly with the venv Python (recommended if you don't want to activate):

```bash
./.venv/bin/python -m pytest -v
```

Running tests this way ensures the correct Python interpreter and site-packages are used and avoids PYTHONPATH-related import errors across different shells.

Running tagged tests
-------------------

You can tag tests using pytest markers (for example: `@pytest.mark.regression`). To run only tests with the `regression` marker:

```bash
# with venv activated
pytest -v -m regression

# or without activating
./.venv/bin/python -m pytest -v -m regression
```

To run everything except regression tests:

```bash
pytest -v -m "not regression"
```

Marker registration note
------------------------
If you see warnings about unknown markers, add the marker to `pytest.ini` to register it. Example `pytest.ini` entry:

```ini
[pytest]
markers =
  regression: mark a test as part of the regression suite
addopts = -v --html=report.html --self-contained-html
```

Adding the marker prevents pytest from emitting "PytestUnknownMarkWarning" and documents the purpose of the marker for your team.

## Common troubleshooting

- ImportError (module not found)
  - Ensure the venv is activated: `source .venv/bin/activate`.
  - Confirm packages are installed: `pip list` (or `./.venv/bin/python -m pip list`).
  - If a package is missing, install it: `pip install <package>`.

- Version mismatches
  - To pin exact versions for reproducibility, run:
    ```bash
    ./.venv/bin/python -m pip freeze > requirements.txt
    ```
    Note: This will overwrite `requirements.txt` with exact installed versions.

- Tests failing because of missing environment variables
  - Create or update `.env` with required keys and re-run tests.