FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry==1.6.1

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . ./

RUN mkdir /cron
RUN touch /cron/django_cron.log

RUN apt update && \
    apt-get install -y cron && \
    apt-get clean

# RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

# CMD ["/app/docker-entrypoint.sh"]
CMD service cron start && python manage.py runserver 0.0.0.0:8000
