#!/bin/bash

# Ждем, пока база данных будет доступна
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Выполняем миграции
python manage.py migrate

# Запускаем сервер
python manage.py runserver 0.0.0.0:8000 