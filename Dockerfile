FROM python:3.10-slim-bullseye

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY . .

# Создание необходимых папок
RUN mkdir logs && mkdir cache

# Переменные окружения
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

# Порт приложения
EXPOSE 5000

# Команда запуска
CMD ["gunicorn", "-w", "4", "--timeout", "30", "-b", "0.0.0.0:5000", "wsgi:app"]