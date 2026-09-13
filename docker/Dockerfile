# Dockerfile for clean-room reproducible builds

FROM python:3.11.6-slim

# Install minimal system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    gnupg \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy pinned requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy source
COPY . /app

ENV PYTHONUNBUFFERED=1

# Default entrypoint is to run tests for verification; runtime images should override
CMD ["pytest", "-q"]
