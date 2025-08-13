# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a modernized Flask web application that serves Futurama quotes with both a web interface and RESTful API. The application has been completely refactored to follow modern Python practices, including type hints, comprehensive testing, and production-ready architecture.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Management
```bash
# Initialize database schema
python manage_db.py init

# Load quotes from futurama_quotes.txt
python manage_db.py load

# Add sample quotes for development/testing
python manage_db.py sample

# Show database statistics
python manage_db.py stats
```

### Running the Application
```bash
# Development server
python app.py

# Production with Gunicorn
gunicorn "app:create_app()" --bind 0.0.0.0:8000
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run tests excluding slow ones
pytest -m "not slow"
```

### Code Quality
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .
```

## Architecture

### Application Factory Pattern

The application uses the factory pattern with environment-specific configurations:

- **app.py**: Main application factory with `create_app()` function
- **config.py**: Environment-specific configuration classes (Development, Testing, Production)
- **models.py**: SQLAlchemy models with modern syntax and type hints

### API Structure

- **api/**: Package containing all API-related modules
- **api/quotes.py**: RESTful API endpoints with Flask-RESTX for automatic documentation
- Full CRUD operations with proper error handling and validation
- Pagination, filtering, and search capabilities

### Database Architecture

- **Modern SQLAlchemy 2.0** syntax with mapped_column and type annotations
- **Single Quote model** with timestamp mixin for audit trails
- **Proper relationships** and query methods
- **Database utilities** in manage_db.py for common operations

### Testing Framework

- **pytest** with comprehensive test coverage
- **Test fixtures** in conftest.py for common test data
- **Separate test files** for models, API, and main app functionality
- **Coverage reporting** with HTML and terminal output

## API Endpoints

### Core Endpoints
- `GET /api/quotes/` - List quotes (with pagination, filtering, search)
- `POST /api/quotes/` - Create new quote
- `GET /api/quotes/{id}` - Get specific quote
- `PUT /api/quotes/{id}` - Update quote
- `DELETE /api/quotes/{id}` - Delete quote
- `GET /api/quotes/random` - Get random quote
- `GET /api/quotes/characters` - List all characters

### Query Parameters
- `page`, `per_page` - Pagination
- `character` - Filter by character
- `search` - Search in quote text

### Documentation
- Automatic API documentation at `/api/`
- Swagger UI with request/response schemas
- Example requests and responses

## File Structure

```
futurama_quote_machine/
├── app.py                 # Application factory
├── config.py              # Configuration classes  
├── models.py              # Database models
├── manage_db.py           # Database utilities
├── requirements.txt       # Dependencies
├── pyproject.toml         # Project configuration
├── .flake8               # Linting configuration
├── api/                  # API package
│   ├── __init__.py
│   └── quotes.py         # Quote endpoints
├── tests/                # Test suite
│   ├── conftest.py       # Test fixtures
│   ├── test_app.py       # App tests
│   ├── test_models.py    # Model tests
│   └── test_api.py       # API tests
├── static/               # Static assets
├── templates/            # Jinja2 templates
└── migrations/           # Database migrations
```

## Development Notes

### Code Quality Standards
- **Type hints**: All functions and methods have complete type annotations
- **Docstrings**: Google-style docstrings for all public methods
- **Error handling**: Proper exception handling with logging
- **Testing**: Minimum 90% test coverage requirement
- **Formatting**: Black code formatting with 88-character line length

### Database Considerations
- Uses SQLAlchemy 2.0 modern syntax
- Timestamp mixin for audit trails
- Proper indexing on frequently queried fields
- Transaction management with proper rollback handling

### API Design Principles
- RESTful endpoint design
- Consistent error responses
- Comprehensive input validation
- Proper HTTP status codes
- Pagination for list endpoints

### Configuration Management
- Environment-based configuration classes
- Secure secret key handling
- Database URL configuration for different environments
- Logging configuration per environment

### Security Features
- Input validation and sanitization
- SQL injection protection via SQLAlchemy ORM
- Proper error message handling (no sensitive data leakage)
- Environment-specific security settings

## Common Development Tasks

### Adding New Quote Fields
1. Update `Quote` model in `models.py`
2. Create database migration
3. Update API schemas in `api/quotes.py`
4. Add validation logic
5. Update tests

### Adding New API Endpoints
1. Add endpoint to `api/quotes.py`
2. Define request/response models
3. Implement service logic
4. Add comprehensive tests
5. Update API documentation

### Running Quality Checks
Always run before committing:
```bash
black . && isort . && flake8 . && mypy . && pytest
```

### Database Migrations
When using Flask-Migrate:
```bash
flask db init      # Initialize migrations
flask db migrate   # Create migration
flask db upgrade   # Apply migration
```