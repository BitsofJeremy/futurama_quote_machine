# Futurama Quote Machine

A modern Flask web application that serves Futurama quotes with both a web interface and RESTful API. Completely refactored with modern Python practices, comprehensive testing, and production-ready features.

## 🚀 Futurama Quote Machine Screenshot

Frontend:
![screenshot.png](screenshot.png)

API:
![screenshot_api.png](screenshot_api.png)

## ✨ Features

- 🎭 **Web Interface**: Clean, responsive web interface displaying random Futurama quotes with character images
- 🚀 **RESTful API**: Full CRUD operations with automatic documentation
- 🔍 **Search & Filter**: Search quotes by text or filter by character
- 📖 **Pagination**: Efficient pagination for large quote collections
- 🎲 **Random Quotes**: Get random quotes via web interface or API
- 🏥 **Health Monitoring**: Built-in health check endpoints
- 🧪 **Comprehensive Testing**: Full test suite with >90% coverage
- 📝 **Type Safety**: Complete type annotations and mypy support
- 🎨 **Code Quality**: Black formatting, flake8 linting, isort imports

## 🛠️ Technology Stack

- **Backend**: Flask 3.0, SQLAlchemy 2.0, Flask-RESTX
- **Database**: SQLite (development), configurable for production
- **Testing**: pytest, pytest-flask, pytest-cov
- **Code Quality**: black, flake8, mypy, isort
- **Type Hints**: Full Python 3.11+ type annotations

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip or poetry for dependency management

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/BitsofJeremy/futurama_quote_machine.git
   cd futurama_quote_machine
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database and load sample data**
   ```bash
   python manage_db.py init
   python manage_db.py sample
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Web interface: http://127.0.0.1:5000
   - API documentation: http://127.0.0.1:5000/api
   - Health check: http://127.0.0.1:5000/health

## 🔧 Configuration

The application supports multiple environments through configuration classes:

### Environment Variables

```bash
# Application settings
FLASK_ENV=development          # development, testing, production
SECRET_KEY=your-secret-key     # Required for production
DATABASE_URL=sqlite:///app.db  # Database connection string

# Server settings
FLASK_HOST=127.0.0.1          # Host to bind to
FLASK_PORT=5000               # Port to listen on
```

### Configuration Files

- `config.py`: Environment-specific configuration classes
- `.env`: Local environment variables (create from example)

## 📊 Database Management

Use the `manage_db.py` script for database operations:

```bash
# Initialize database schema
python manage_db.py init

# Load quotes from futurama_quotes.txt
python manage_db.py load

# Add sample quotes for development
python manage_db.py sample

# Show database statistics
python manage_db.py stats
```

## 🌐 API Endpoints

### Quotes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/quotes/` | List all quotes (with pagination) |
| `POST` | `/api/quotes/` | Create a new quote |
| `GET` | `/api/quotes/{id}` | Get a specific quote |
| `PUT` | `/api/quotes/{id}` | Update a quote |
| `DELETE` | `/api/quotes/{id}` | Delete a quote |
| `GET` | `/api/quotes/random` | Get a random quote |
| `GET` | `/api/quotes/characters` | List all characters |

### Query Parameters

- `page`: Page number for pagination (default: 1)
- `per_page`: Items per page (default: 20, max: 100)
- `character`: Filter by character name
- `search`: Search in quote text

### Example API Usage

```bash
# Get all quotes
curl http://localhost:5000/api/quotes/

# Get quotes by character
curl "http://localhost:5000/api/quotes/?character=Bender"

# Search quotes
curl "http://localhost:5000/api/quotes/?search=money"

# Get random quote
curl http://localhost:5000/api/quotes/random

# Create new quote
curl -X POST http://localhost:5000/api/quotes/ \\
  -H "Content-Type: application/json" \\
  -d '{"quote_text": "New quote", "character": "Character"}'
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run tests with verbose output
pytest -v

# Run only fast tests (skip slow/integration tests)
pytest -m "not slow"
```

### Test Structure

- `tests/conftest.py`: Pytest fixtures and configuration
- `tests/test_app.py`: Main application tests
- `tests/test_models.py`: Database model tests
- `tests/test_api.py`: API endpoint tests

## 🎨 Code Quality

### Running Code Quality Tools

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .

# Type check with mypy
mypy .

# Run all quality checks
make quality  # If using Makefile
```

### Pre-commit Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 📁 Project Structure

```
futurama_quote_machine/
├── app.py                 # Main application factory
├── config.py              # Configuration classes
├── models.py              # Database models
├── manage_db.py           # Database management utilities
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── .flake8               # Flake8 configuration
├── api/                  # API package
│   ├── __init__.py
│   └── quotes.py         # Quote API endpoints
├── tests/                # Test suite
│   ├── __init__.py
│   ├── conftest.py       # Test configuration
│   ├── test_app.py       # App tests
│   ├── test_models.py    # Model tests
│   └── test_api.py       # API tests
├── static/               # Static assets
│   ├── css/
│   └── img/
├── templates/            # Jinja2 templates
│   └── index.html
└── migrations/           # Database migrations (if using Flask-Migrate)
```

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-very-secure-secret-key
   export DATABASE_URL=postgresql://user:pass@host:port/dbname
   ```

2. **Database Setup**
   ```bash
   flask db upgrade  # Run migrations
   python manage_db.py load  # Load initial data
   ```

3. **WSGI Server**
   ```bash
   # Using Gunicorn
   pip install gunicorn
   gunicorn "app:create_app()" --bind 0.0.0.0:8000
   ```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage_db.py init && python manage_db.py sample

EXPOSE 5000
CMD ["python", "app.py"]
```

## 🔄 Migration from Legacy Version

If upgrading from the old version:

1. **Backup your data**
   ```bash
   cp futurama_quote_machine.db futurama_quote_machine.db.backup
   ```

2. **Install new dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **The new version uses the same database structure** - your existing data should work as-is

4. **Update any custom integrations** to use the new API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run quality checks (`black .`, `flake8 .`, `mypy .`, `pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📋 Development Workflow

```bash
# Setup development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Initialize database
python manage_db.py init
python manage_db.py sample

# Run tests
pytest

# Start development server
python app.py

# Format and lint code
black .
isort .
flake8 .
mypy .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original Futurama quotes and characters © 20th Century Fox
- Flask and the wonderful Python community
- All contributors and users of this project

## 📈 Version History

- **v2.0.0**: Complete modernization with Flask 3.0, type hints, comprehensive testing
- **v1.0.0**: Original Flask application with basic functionality

## 🐛 Issues & Support

- [Report bugs](https://gitlab.com/deafmice/futurama_quote_machine/-/issues)
- [Request features](https://gitlab.com/deafmice/futurama_quote_machine/-/issues)
- [View documentation](https://gitlab.com/deafmice/futurama_quote_machine/-/wikis/home)