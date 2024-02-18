#!/bin/bash

# Добавляем права на запись для лог-файла Django Cron
chmod +w /cron/django_cron.log

# Добавляем задания Cron
python manage.py crontab add

# Запускаем сервис Cron в фоновом режиме
service cron start

# Применяем миграции базы данных Django
python manage.py makemigrations
python manage.py migrate

# Создаем суперпользователя Django, если его нет
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Запускаем скрипт обновления курсов валют
python manage.py update_rate

# Запускаем Django сервер
python manage.py runserver 0.0.0.0:8000
