# Multi-stage Dockerfile for Flask application

# Build stage
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash flask

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=flask:flask src/ ./src/
COPY --chown=flask:flask pyproject.toml ./

# Create necessary directories
RUN mkdir -p /app/logs /app/instance && \
    chown -R flask:flask /app

# Switch to non-root user
USER flask

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--worker-class", "gevent", "--worker-connections", "1000", "--timeout", "120", "--keepalive", "5", "--max-requests", "1000", "--max-requests-jitter", "50", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-", "src.app:app"]
