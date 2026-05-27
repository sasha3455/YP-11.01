# YP-11.01 — интернет-магазин одежды (Django)

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp shop/.env.example shop/.env
# отредактируйте shop/.env под свою PostgreSQL

cd shop
python manage.py migrate
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/  
Админка: http://127.0.0.1:8000/admin/

## Структура

- `shop/` — Django-проект
- `shop/djS0rrow/` — приложение магазина (модели, views, urls, templates)
