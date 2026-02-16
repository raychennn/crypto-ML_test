FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for numpy/pandas compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory (will be overridden by persistent volume)
RUN mkdir -p /data

# Environment variables
ENV DATA_ROOT=/data
ENV TZ=Asia/Taipei
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Health check for Zeabur / container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1

# Default: run bot + scheduler + web dashboard
CMD ["python", "main.py", "serve", "--components", "all"]
