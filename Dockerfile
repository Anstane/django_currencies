FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry==1.6.1

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . ./

RUN mkdir /app/cron
RUN touch /app/cron/django_cron.log

RUN apt update && \
    apt install -y cron && \
    apt install -y dos2unix && \
    apt install -y curl

RUN chmod +x /app/docker-entrypoint.sh

RUN dos2unix /app/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]
