FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# --- FIX IS HERE: Add libpq-dev to apt-get install ---
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# ---------------------------------------------------

COPY requirements.txt .

# 1. Upgrade pip first (optional but good practice)
RUN pip install --upgrade pip

# 2. Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# ... rest of the Dockerfile ...
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]

