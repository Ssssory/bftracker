from django.urls import path

from .views import *

urlpatterns = [
    path('test', test),
    path('point/', points),
    path('', dashboard),
    path('settings/', config),
]
