from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('point/', points),
    path('dashboard/22/', dashboard),
    path('settings/', config),



    path('myadmin/dashboard', admin_dashboard),
    path('myadmin/<int:owner>/<int:point>', admin_dashboard_point_stat),
]
