from django.urls import path

from .views import index, currencies

urlpatterns = [
    path('', index, name='index'),
    path('currencies/', currencies, name='currencies'),
]
