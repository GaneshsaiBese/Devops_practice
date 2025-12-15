# Stage 1: Build stage
FROM python:3.11-alpine AS builder
WORKDIR /app

RUN apk update && apk add --no-cache build-base libffi-dev \
    && python -m ensurepip --upgrade \
    && pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Minimal runtime image
FROM python:3.11-alpine AS runtime

WORKDIR /app

RUN apk update && apk add --no-cache libssl3 \
    && rm -rf /var/cache/apk/*

# --- FIX IS HERE ---
# 1. Copy your application source code
COPY --from=builder /app /app

# 2. Explicitly copy the Python packages directory from the builder stage
# This path is standard for Python 3.11 on Alpine
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# -------------------

EXPOSE 8501

CMD ["python","-m","streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

