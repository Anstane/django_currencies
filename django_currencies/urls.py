from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('rate/', include('rate.urls')),
    path('admin/', admin.site.urls),
]
