# Flask-Minimal 2.0 🚀

A **modern, production-ready Flask library management system** template showcasing current industry best practices. This template provides a solid foundation for building scalable Flask applications with enterprise-grade features.

[![Flask](https://img.shields.io/badge/Flask-3.1.1-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-green.svg)](https://sqlalchemy.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

### 🏗️ **Modern Architecture**
- **Application Factory Pattern** with environment-based configuration
- **Service Layer Architecture** with proper separation of concerns
- **SQLAlchemy 2.0 ORM** with database migrations (Flask-Migrate)
- **RESTful API** with versioning (v1) and OpenAPI-ready structure

### 🔒 **Security & Authentication**
- **JWT Authentication** with refresh tokens
- **Role-Based Access Control (RBAC)** - Admin/User roles
- **Bcrypt Password Hashing** for secure password storage
- **Rate Limiting** to prevent abuse
- **CORS Support** for cross-origin requests

### 📊 **Data Management**
- **PostgreSQL/SQLite Support** with connection pooling
- **Database Migrations** with Alembic
- **Model Relationships** (Users, Books, Loans with borrowing system)
- **Data Validation** with Marshmallow schemas
- **Pagination & Search** capabilities

### 🐳 **DevOps & Deployment**
- **Multi-stage Docker** builds for optimization
- **Docker Compose** for local development
- **Production WSGI** server (Gunicorn) configuration
- **Health Check** endpoints for monitoring
- **Environment Configuration** management

### 🧪 **Developer Experience**
- **CLI Commands** for database management and seeding
- **Modern Python Packaging** with pyproject.toml
- **Type Hints** throughout codebase
- **Comprehensive Error Handling** with custom exceptions
- **Structured Logging** ready

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker (optional but recommended)
- Git

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/djeada/Flask-Minimal.git
cd Flask-Minimal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# Key variables:
# - SECRET_KEY: Your application secret key
# - JWT_SECRET_KEY: JWT signing key
# - DATABASE_URL: Database connection string
```

### 3. Initialize Database

```bash
# Set Flask app
export FLASK_APP=src.app:app

# Initialize database
flask init-db

# Seed with sample data
flask seed-db
```

### 4. Run the Application

```bash
# Development server
flask run --host=0.0.0.0 --port=5000

# Or using Python directly
python src/app.py
```

The application will be available at `http://localhost:5000`

## 🐳 Docker Development

For a complete development environment with PostgreSQL and Redis:

```bash
# Start all services
docker-compose up --build

# Initialize database (first time only)
docker-compose exec web flask init-db
docker-compose exec web flask seed-db
```

Services:
- **Web App**: http://localhost:5000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 📚 API Documentation

### Authentication

#### Register User
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@library.com",
    "password": "admin123"
  }'
```

#### Get Current User
```bash
curl -X GET http://localhost:5000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Books Management

#### List Books (with search)
```bash
# Get all books
curl http://localhost:5000/api/v1/books

# Search books
curl "http://localhost:5000/api/v1/books?search=tolkien&page=1&per_page=10"
```

#### Get Book Details
```bash
curl http://localhost:5000/api/v1/books/1
```

#### Create Book (Admin only)
```bash
curl -X POST http://localhost:5000/api/v1/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "year": 1925,
    "isbn": "9780743273565",
    "total_copies": 3
  }'
```

#### Borrow Book
```bash
curl -X POST http://localhost:5000/api/v1/books/1/borrow \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer USER_JWT_TOKEN" \
  -d '{"days": 14}'
```

#### Return Book
```bash
curl -X POST http://localhost:5000/api/v1/books/loans/1/return \
  -H "Authorization: Bearer USER_JWT_TOKEN"
```

### User Management

#### List Users (Admin only)
```bash
curl http://localhost:5000/api/v1/users \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN"
```

#### Get User Loans
```bash
curl http://localhost:5000/api/v1/users/1/loans \
  -H "Authorization: Bearer USER_JWT_TOKEN"
```

### Health Check
```bash
curl http://localhost:5000/health
```

## 🏗️ Project Structure

```
Flask-Minimal/
├── src/
│   ├── __init__.py              # Application factory
│   ├── app.py                   # Application entry point
│   ├── config.py                # Configuration management
│   ├── extensions.py            # Flask extensions
│   ├── exceptions.py            # Custom exceptions
│   ├── cli.py                   # CLI commands
│   ├── api/
│   │   ├── v1/                  # API version 1
│   │   │   ├── __init__.py      # API blueprint registration
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── users.py         # User management endpoints
│   │   │   └── books.py         # Book management endpoints
│   │   ├── decorators.py        # API decorators
│   │   └── errors.py            # Error handlers
│   ├── models/
│   │   └── __init__.py          # Database models
│   ├── services/
│   │   ├── user_service.py      # User business logic
│   │   └── book_service.py      # Book business logic
│   ├── web/
│   │   └── __init__.py          # Web interface blueprints
│   └── templates/               # Jinja2 templates
├── tests/                       # Test suite
├── migrations/                  # Database migrations
├── docker-compose.yml           # Development environment
├── Dockerfile                   # Production container
├── pyproject.toml              # Modern Python packaging
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🧪 Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 🚀 Production Deployment

### Environment Variables

```bash
# Required production environment variables
FLASK_ENV=production
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
```

### Using Docker

```bash
# Build production image
docker build -t flask-minimal:latest .

# Run container
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DATABASE_URL=postgresql://... \
  flask-minimal:latest
```

### Database Migration

```bash
# Initialize migrations (first time)
flask db init

# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade
```

## 🛠️ CLI Commands

```bash
# Database management
flask init-db              # Initialize database tables
flask seed-db              # Seed with sample data
flask create-admin          # Create admin user

# Database migrations
flask db init              # Initialize migrations
flask db migrate           # Create migration
flask db upgrade           # Apply migrations
flask db downgrade         # Rollback migrations
```

## 🔧 Configuration

### Environment-based Configuration

The application supports multiple environments:

- **Development**: SQLite database, debug mode enabled
- **Testing**: In-memory database, testing optimizations
- **Production**: PostgreSQL database, security hardened

### Key Configuration Options

```python
# Security
SECRET_KEY                    # Flask secret key
JWT_SECRET_KEY               # JWT signing key
BCRYPT_LOG_ROUNDS           # Password hashing rounds

# Database
DATABASE_URL                 # Database connection string
SQLALCHEMY_ENGINE_OPTIONS   # SQLAlchemy engine options

# Rate Limiting
RATELIMIT_STORAGE_URL       # Rate limiting storage backend

# Pagination
ITEMS_PER_PAGE              # Default items per page
MAX_ITEMS_PER_PAGE          # Maximum items per page
```

## 📖 Architecture Overview

### Application Factory Pattern
The application uses the factory pattern for better testability and configuration management.

### Service Layer
Business logic is separated into service classes, making the code more maintainable and testable.

### Repository Pattern
Data access is abstracted through SQLAlchemy models with service layer coordination.

### JWT Authentication
Stateless authentication using JSON Web Tokens with role-based access control.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run code quality checks
black src tests
isort src tests
flake8 src tests
mypy src
bandit -r src
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask team for the excellent web framework
- SQLAlchemy team for the powerful ORM
- All contributors and users of this template

---

**Flask-Minimal 2.0** - Building modern Flask applications with confidence! 🚀
