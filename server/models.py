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
    closed_at = models.DateTimeField(blank=True)

class Point(models.Model):
    restaurant = models.ForeignKey(Restaurant,related_name="point")
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True)


class Client(models.Model):
    messenger_id = models.CharField(max_length=30)
    messenger_type = models.CharField(max_length=15)
    phone = models.CharField(max_length=12, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    external_id = models.CharField(max_length=50, blank=True)
    order_id = models.CharField(max_length=30)
    client = models.ForeignKey(Client)
    point = models.ForeignKey(Point)
    status_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderStatusesHistory(models.Model):
    order = models.ForeignKey(Order,related_name="status_history")
    status_id = models.PositiveIntegerField()
    date_start = models.DateTimeField()
    duration = models.PositiveIntegerField()


class NotificationText(models.Model):
    point = models.ForeignKey(Point)
    message = models.TextField()
    type = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

class Notification(models.Model):
    client = models.ForeignKey(Client, related_name="notifications")
    order = models.ForeignKey(Order)
    text = models.ForeignKey(NotificationText)
    date_send = models.DateTimeField()



