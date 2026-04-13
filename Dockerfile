# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build essentials and system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Upgrade pip, setuptools, wheel and install with binary wheels preference
RUN pip install --upgrade pip setuptools wheel && \
    pip install --prefer-binary -r requirements.txt

# Copy application code
COPY config.py .
COPY logger_config.py .
COPY data.py .
COPY strategy.py .
COPY notifier.py .
COPY scheduler.py .
COPY market_hours.py .
COPY backtest.py .
COPY demo_data.py .
COPY main.py .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:10000/health', timeout=5)" || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
