#!/bin/bash

chmod +w /cron/django_cron.log
python manage.py crontab add
service cron start

python manage.py makemigrations
python manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
python manage.py update_rate
python manage.py runserver 0.0.0.0:8000
