#!/bin/bash
set -e

echo "Ожидание PostgreSQL..."
until python -c "
import os, socket
host = os.environ.get('DB_HOST_PGSQL', 'db')
port = int(os.environ.get('DB_PORT_PGSQL', 5432))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try:
    s.connect((host, port))
    s.close()
    raise SystemExit(0)
except Exception:
    raise SystemExit(1)
"; do
  echo "БД недоступна, повтор через 2 сек..."
  sleep 2
done

echo "Миграции..."
python manage.py migrate --noinput

echo "Сбор статики..."
python manage.py collectstatic --noinput

echo "Создание суперпользователя (если задан в .env)..."
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Суперпользователь {username} создан')
"

echo "Запуск Gunicorn..."
exec gunicorn shop.wsgi:application --bind 0.0.0.0:8000 --workers 4
