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

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000

CMD ["/docker-entrypoint.sh"]
