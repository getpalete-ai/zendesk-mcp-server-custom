# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

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

# Expose port (using port 8021 to avoid conflicts)
EXPOSE 8021

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8021/status')" || exit 1

# Set default environment variables (these should be overridden in production)
ENV ZENDESK_BASE_URL="" \
    ZENDESK_EMAIL="" \
    ZENDESK_API_TOKEN=""

# Run the application
CMD ["python", "mcp_zendesk/server.py"]
