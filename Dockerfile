FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends       build-essential default-libmysqlclient-dev pkg-config     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN mkdir -p /app/static /app/media

CMD ["gunicorn", "PaginationProject.wsgi:application", "-b", "0.0.0.0:8000", "--workers", "3"]
