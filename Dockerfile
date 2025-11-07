FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

COPY b2b_portal/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY b2b_portal /app

RUN mkdir -p /app/media /app/staticfiles

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
