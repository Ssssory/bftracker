from django.urls import path

from .views import *
from .api_views import *

urlpatterns = [
    path('jsonrpc', run),  # jsonrpc
    # android rest
    path('auth', auth),
    path('order', order),
    path('link', link),
    path('status', status),
    path('list', list),
]
