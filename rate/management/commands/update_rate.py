import requests
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from rate.models import Currency

class Command(BaseCommand):
    help = 'Обновляем данные о валютах.'

    def handle(self, *args, **kwargs):
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.get(url)
        data = response.json() # Получаем данные о валютах

        date_str = data['Date'][:10]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() # Вытягиваем и форматируем поле даты.

        # Безопасно проверяем наличие записей в БД с текущей датой.
        existing_currencies = Currency.objects.select_for_update().filter(date=date_obj)

        currencies_to_update = [] # Сюда все существующие в БД данные.
        currencies_to_create = [] # Данные, которые мы будем вставлять в БД.

        # Создаём словарь, чтобы уменьшить количество запросов к БД.
        existing_currency_dict = {currency.charcode: currency for currency in existing_currencies}

        for charcode, value in data['Valute'].items(): # В цикле перебираем ответ от API.
    
            if charcode in existing_currency_dict: # Если есть в БД -> отправляется на обновление.
                existing_currency = existing_currency_dict[charcode]
                existing_currency.rate = value['Value']
                currencies_to_update.append(existing_currency)

            else: # Если такой записи ещё нет в БД -> отправляется на добавление.
                currencies_to_create.append(
                    Currency(
                        charcode=charcode,
                        date=date_obj,
                        rate=value['Value']
                    )
                )

        with transaction.atomic(): # Делаем запись в БД атомарной.
            Currency.objects.bulk_update(currencies_to_update, ['rate'])
            Currency.objects.bulk_create(currencies_to_create)

        self.stdout.write(self.style.SUCCESS('Данные были успешно обновлены.'))
