from server.models import Point
from django.db import models

from uuid import uuid4
from django.utils import timezone
from datetime import timedelta


# Create your models here.


class ApiTimeToken(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def getOrCreateToken(cls, point):
        today = timezone.now()
        yesteryday = today + timedelta(days=-1)
        raw = cls.objects.filter(point=point, created_at__gt=yesteryday)
        if raw.exists():
            return raw[0].token
        else:
            # удалим все протухшие ключи
            cls.objects.filter(point=point).delete()
            # создадим новую запись
            token = uuid4()
            newToken = ApiTimeToken(point=point, token=token)
            newToken.save()
            return token
