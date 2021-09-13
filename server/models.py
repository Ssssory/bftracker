from django.conf import settings
from django.db import models


class Restaurant(models.Model):
    login = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, blank=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=90, blank=True)
    ul = models.CharField(max_length=200, blank=True)
    inn = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(auto_now_add=True)

    def as_json(self):
        return dict(
            id=self.pk,
            login=self.login, 
            email=self.email,
            name=self.name,
            city=self.city,
            ul=self.ul,
            inn=self.inn,
            created_at=self.created_at)

class Point(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="point", on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(auto_now_add=True)
    def as_json(self):
        return dict(
            id=self.pk,
            login=self.login,
            address=self.address,
            name=self.name,
            created_at=self.created_at.strftime(settings.DATE_FORMAT))


class Client(models.Model):
    messenger_id = models.CharField(max_length=30)
    messenger_type = models.CharField(max_length=15)
    phone = models.CharField(max_length=12, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    external_id = models.CharField(max_length=50, blank=True)
    order_id = models.CharField(max_length=30)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=True, null=True)
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def as_json(self):
        return dict(
            # id=self.pk,
            order_id=self.order_id,
            external_id=self.external_id,
            status=self.status,
            created_at=self.created_at.strftime(settings.DATE_FORMAT))


class OrderStatusesHistory(models.Model):
    order = models.ForeignKey(Order,related_name="status_history", on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    date_start = models.DateTimeField()
    duration = models.PositiveIntegerField()


class NotificationText(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

class Notification(models.Model):
    client = models.ForeignKey(Client, related_name="notifications", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    text = models.ForeignKey(NotificationText, on_delete=models.CASCADE)
    date_send = models.DateTimeField()



