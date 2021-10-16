import json
import collections
from server.classes.status import Status
from api.models import ApiTimeToken
from django.conf import settings
from datetime import date, datetime, time, timedelta, timezone

from django.contrib.auth.hashers import MD5PasswordHasher
from server.models import Order, Point
from bot.helper.telegram import TelegramServise
from bot.helper.messages import Messages

class Logic:

    def getHeaderAuth(self, request):
        token = request.headers.get('Authorization')
        # today = timezone.now()
        # yesteryday = today + timedelta(days=-1)
        if token is None:
            raise Exception('no token')
        auth = ApiTimeToken.objects.filter(token=token)
        # auth = ApiTimeToken.objects.filter(token=token, created_at__gt=yesteryday)
        if auth.exists():
            return auth
        raise Exception('token timeout')

    def getparam(self, request, param=None):
        # разбираем json в []
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if param != None:
            if collections.Counter(param) != collections.Counter(body.keys()):
                raise Exception('all fields required')
        return body

    def auth(self, request):
        # принимаем только запросы методом POST
        if request.method != 'POST':
            raise Exception('error HTTP method')
        arBody = self.getparam(request, ['login', 'password'])

        login = arBody['login']
        password = arBody['password']
        point = Point.objects.get(login=login)
        # проверяем корректность пароля
        if point.password == MD5PasswordHasher().encode(
                str(password), settings.SALT):
            token = ApiTimeToken.getOrCreateToken(point)
            return {"token": token, "point": point.as_json()}
        else:
            raise Exception('incorrect login or password')

    def order(self, request, auth):
        # принимаем только запросы методом POST
        if request.method != 'POST':
            raise Exception('error HTTP method')

        arBody = self.getparam(request, ['order'])
        order = arBody['order']

        newOrder = Order(
            order_id=order,
            client=None,
            point=auth[0].point,
            status=Status.NEW
        )
        newOrder.save()

        return newOrder.as_json()

    def link(self, request, auth):
        # принимаем только запросы методом POST
        if request.method != 'GET':
            raise Exception('error HTTP method')

        point = auth[0].point
        link = settings.BOT_LINK
        return {"link": link, "point": point.as_json()}

    # TODO: прикрутить проверку на номер заказа по точке
    def status(self, request, auth):
        # принимаем только запросы методом POST
        if request.method != 'POST':
            raise Exception('error HTTP method')

        arBody = self.getparam(request, ['order_id', 'status'])
        order = arBody['order_id']
        status = arBody['status']

        today = date.today()

        order = Order.objects.get(order_id=order, point=auth[0].point, created_at__gt=today)
        if status == Status.READY:
            if order.client:
                telegram = TelegramServise()
                telegram.send_message(
                    order.client, Messages.default_ready_text)
        order.status = status
        order.save()

        return order.as_json()

    def list(self, request, auth):
        # принимаем только запросы методом POST
        if request.method != 'GET':
            raise Exception('error HTTP method')

        today_min = datetime.combine(date.today(), time.min)
        today_max = datetime.combine(date.today(), time.max)
        statuslist = list([Status.IN_PROGRESS, Status.READY, Status.NEW, Status.CALL])
        orders = Order.objects.filter(
            point=auth[0].point, status__in=statuslist, created_at__range=(today_min, today_max))
        if orders.exists():
            result = list()
            for raw in orders:
                result.append(raw.as_json())
            return {"orders": result}
        else:
            return {"orders": {}}
