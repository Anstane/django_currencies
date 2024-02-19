from datetime import date

from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse

from .models import Currency

def index(request):
    """
    Функция для получения данных о валюте.

    Ожидаемый запрос: /rate/?charcode=AUD&date=2024-01-01
    charcode - наименование валюты
    date - дата в формате YY-MM-DD

    Получаем из GET-запроса данные и отталкиваясь от них возвращаем JSON.
    """

    charcode = request.GET.get('charcode')
    date = request.GET.get('date')

    currency = Currency.objects.filter(charcode=charcode, date=date).first()

    if currency:
        return JsonResponse({
            'charcode': currency.charcode,
            'date': currency.date,
            'rate': currency.rate,
        })
    else:
        return HttpResponseNotFound('<h1>Валюта не обнаружена</h1>')

    # return render(request, 'main/index.html', context) Если нужно получать данные не JSON, а HTML.

def currencies(request):
    """Функция для отображения всех курсов за текущую дату."""

    today = date.today()
    currencies = Currency.objects.filter(date=today)

    context = {
        'today': today,
        'currencies': currencies,
    }

    return render(request, 'main/currencies.html', context)
