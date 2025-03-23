FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv for dependency management
RUN pip install --no-cache-dir uv

# Copy only dependency files to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv pip install --system --no-cache .

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Second stage for a leaner final image
FROM python:3.11-slim AS runtime

WORKDIR /app

# Create non-root user in the runtime image
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the app code
COPY --chown=appuser:appuser src/ ./src/

# Switch to the non-root user
USER appuser

# Set Python path to include the app src directory
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD ["python", "-c", "import requests; requests.get('http://localhost:8000/health')"]

# Run the app
CMD ["python", "-m", "finetune.cli", "--help"]
