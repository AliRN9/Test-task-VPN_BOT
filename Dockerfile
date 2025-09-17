FROM python:3.12-slim

WORKDIR /app

# Ускоряем Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Alembic для миграций
RUN pip install --no-cache-dir alembic


COPY requirements.txt ./


RUN pip install -r  requirements.txt


COPY . /app


# Запуск бота
CMD ["python3", "-m", "app.main"]
