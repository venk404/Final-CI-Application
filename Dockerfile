FROM python:3.13-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache postgresql-dev=16.4-r0 gcc=13.2.1_git20240309-r0 musl-dev=1.2.5-r0
# Create a virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.13-alpine

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /app/venv /app/venv

COPY ./code/ /app/code/

# Set environment variables
ENV PATH="/app/venv/bin:$PATH"

# Install runtime dependencies
RUN apk add --no-cache libpq=16.4-r0


# Expose port 8000

EXPOSE 8000

# Use exec form for CMD
CMD ["python", "code/Main.py"]