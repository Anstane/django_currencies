from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse

from .models import Currency

def index(request):
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

    # return render(request, 'index.html', context) Если нужно получать данные не JSON, а HTML.
