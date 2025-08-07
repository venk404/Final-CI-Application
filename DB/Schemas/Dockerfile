# Build stage
FROM python:3.13-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc=14.2.0-r6 \
    musl-dev=1.2.5-r10 \
    postgresql17-dev=17.5-r0

# Create virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.13-alpine

WORKDIR /app

# Install runtime dependencies
RUN apk add --no-cache libpq=17.5-r0

# Copy the entire virtual environment from builder
COPY --from=builder /app/venv /app/venv

# Set PATH to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy application code
COPY Create_Student.py .

CMD ["python", "Create_Student.py"]