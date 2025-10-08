# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    SERVER_HOST=0.0.0.0 \
    SERVER_PORT=8021

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml setup.cfg ./
COPY mcp_zendesk/ ./mcp_zendesk/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -e .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port (using parameterized port)
EXPOSE ${SERVER_PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:${SERVER_PORT}/status')" || exit 1

# Set default environment variables (these should be overridden in production)
ENV ZENDESK_BASE_URL="" \
    ZENDESK_EMAIL="" \
    ZENDESK_API_TOKEN=""

# Run the application
CMD ["python", "-c", "import sys; sys.path.append('/app'); from mcp_zendesk.server import app; import uvicorn; uvicorn.run(app, host='${SERVER_HOST}', port=${SERVER_PORT})"]
