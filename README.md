# ohtuvarasto
[![CI](https://github.com/Tapir79/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/Tapir79/ohtuvarasto/actions/)

[![codecov](https://codecov.io/github/Tapir79/ohtuvarasto/graph/badge.svg?token=TYZUSTGBQD)](https://codecov.io/github/Tapir79/ohtuvarasto)

A warehouse management system with Flask-based web UI and original Varasto class.

## Features

### Web UI (Flask)
- **Create warehouses**: Add new warehouses with name, capacity, and initial balance
- **List warehouses**: View all warehouses with their current status
- **View warehouse**: See detailed information about a specific warehouse
- **Edit warehouse**: Modify warehouse name, capacity, and balance
- **Add items**: Add items to a warehouse
- **Remove items**: Remove items from a warehouse
- **Delete warehouse**: Remove a warehouse from the system

All operations include:
- Server-side validation
- Client-side validation (real-time feedback)
- Bootstrap styling for responsive design

### Core Library
The original `Varasto` class provides:
- Capacity management (tilavuus)
- Balance tracking (saldo)
- Safe item addition and removal with automatic boundary checks

## Installation

1. Install dependencies:
```bash
poetry install
```

## Running the Web Application

Start the Flask development server:
```bash
poetry run python src/app.py
```

Then open your browser and navigate to `http://localhost:5000`

## Running Tests

Run all tests:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run coverage run --branch -m pytest
poetry run coverage report
```

## Code Quality

Run linter:
```bash
poetry run pylint src
```

Run code formatter:
```bash
poetry run autopep8 --in-place --aggressive --aggressive src/
```

## Project Structure

```
src/
├── app.py                  # Flask web application
├── warehouse_service.py    # Service layer for managing multiple warehouses
├── varasto.py             # Original Varasto class (unchanged)
├── templates/             # Jinja2 templates
│   ├── base.html         # Base template with Bootstrap
│   ├── list.html         # List all warehouses
│   ├── create.html       # Create warehouse form
│   ├── view.html         # View warehouse details
│   └── edit.html         # Edit warehouse form
└── tests/
    ├── varasto_test.py           # Tests for Varasto class
    ├── warehouse_service_test.py # Tests for WarehouseService
    └── flask_routes_test.py      # Tests for Flask routes
```

## Tehtyjen tehtävien dokumentaatio
* [Viikko 1 - Tehtävät 2 - 13](https://github.com/Tapir79/ohtuvarasto/tree/main/dokumentaatio/tehtavat1.md)
* [Viikko 2 - Tehtävät 6 - 8](https://github.com/Tapir79/ohtuvarasto/tree/main/dokumentaatio/tehtavat2.md)