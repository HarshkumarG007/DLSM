FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create dedicated non-root application user
RUN groupadd -g 1001 dlsm && \
    useradd -u 1001 -g dlsm -m -s /bin/bash dlsm

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set ownership to dlsm non-root user
RUN chown -R dlsm:dlsm /app

USER dlsm

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
