from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('point/', points),
    path('dashboard/22/', dashboard),
    path('settings/', config),
]
