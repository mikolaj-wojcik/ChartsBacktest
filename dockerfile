# Use official Python image as base
FROM python:3.11

LABEL authors="mjetur"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r base_user && \
    useradd -r -g base_user -u 1000 base_user && \
    mkdir -p /app && \
    chown -R base_user:base_user /app

# Set working directory
WORKDIR /app

COPY --chown=base_user:base_user requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=base_user:base_user . .

# Switch to non-root user
USER base_user

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]