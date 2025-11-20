# Flask Web UI for Warehouse Management

This is a Flask-based web user interface for managing warehouse objects (Varasto).

## Features

- Create new warehouses with custom capacity and initial balance
- View all warehouses in a card-based layout
- View detailed information about individual warehouses
- Add items to warehouses
- Remove items from warehouses
- Edit warehouse properties (name, capacity, balance)
- Delete warehouses
- Form validation with error messages
- Bootstrap styling for a modern UI
- Progress bars showing capacity usage
- Flash messages for user feedback

## Installation

1. Install dependencies using Poetry:
```bash
poetry install
```

## Running the Application

### Option 1: Using Flask CLI
```bash
cd src
FLASK_APP=app.py poetry run flask run
```

### Option 2: Using Python directly
```bash
cd src
poetry run python app.py
```

The application will be available at http://127.0.0.1:5000/

## Running Tests

Run all tests including the original Varasto tests and new Flask tests:
```bash
poetry run pytest src/tests/ -v
```

## Running Linting

Check code quality with pylint:
```bash
poetry run pylint src/*.py
```

## Project Structure

```
src/
├── app.py                    # Flask application with routes
├── warehouse_service.py      # Service layer for managing warehouses
├── varasto.py               # Original Varasto class (unchanged)
├── templates/               # Jinja2 templates
│   ├── layout.html          # Base template with Bootstrap
│   ├── index.html           # List all warehouses
│   ├── create_warehouse.html # Create warehouse form
│   ├── warehouse_detail.html # View/manage single warehouse
│   └── edit_warehouse.html   # Edit warehouse form
└── tests/
    ├── varasto_test.py      # Original Varasto tests
    └── flask_app_test.py    # Flask application tests
```

## API Routes

- `GET /` - Redirects to `/warehouses`
- `GET /warehouses` - List all warehouses
- `GET /warehouses/new` - Form to create a new warehouse
- `POST /warehouses` - Create a new warehouse
- `GET /warehouses/<id>` - View single warehouse details
- `POST /warehouses/<id>/add` - Add items to warehouse
- `POST /warehouses/<id>/remove` - Remove items from warehouse
- `GET /warehouses/<id>/edit` - Form to edit warehouse
- `POST /warehouses/<id>/edit` - Update warehouse
- `POST /warehouses/<id>/delete` - Delete warehouse

## Design Decisions

- **In-memory storage**: Warehouses are stored in a dictionary, no database required
- **Service layer**: `WarehouseService` provides a clean interface for managing warehouses
- **Unchanged Varasto class**: The original `Varasto` class remains completely unchanged
- **Bootstrap CDN**: Uses Bootstrap 5 from CDN for styling (no local files needed)
- **Form validation**: Both client-side (HTML5) and server-side validation
- **Flash messages**: User feedback for all actions (success/error messages)
- **RESTful design**: Follows REST principles with appropriate HTTP methods

## Notes

- This is a development server. For production, use a production WSGI server like Gunicorn
- The secret key is hardcoded for development. Change it in production
- Data is stored in memory and will be lost when the application restarts
