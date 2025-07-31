# Build stage
FROM python:3.13-alpine as builder

WORKDIR /app

# Install required packages
RUN apk add --no-cache postgresql-dev gcc musl-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.13-alpine

WORKDIR /app

# Install only runtime dependencies
RUN apk add --no-cache libpq

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application
COPY Create_Student.py .

CMD ["python", "Create_Student.py"]