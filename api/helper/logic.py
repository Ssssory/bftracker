import json
import collections
from server.classes.status import Status
from api.models import ApiTimeToken
from django.conf import settings
from datetime import date, datetime, time, timedelta

from django.contrib.auth.hashers import MD5PasswordHasher
from server.models import Order, Point

class Logic:

    def getHeaderAuth(self, request):
        token = request.headers.get('Authorization')
        if token is None:
            raise Exception('no token')
        auth = ApiTimeToken.objects.filter(token=token)
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
        link = "https://t.me/ZhduEduBot?start="
        return {"link": link, "point": point.as_json()}

    # TODO: прикрутить проверку на номер заказа по точке
    def status(self, request, auth):
        # принимаем только запросы методом POST
        if request.method != 'POST':
            raise Exception('error HTTP method')

        arBody = self.getparam(request, ['orderId', 'status'])
        order = arBody['orderId']
        status = arBody['status']

        order = Order.objects.get(order_id=order)
        order.status = status
        order.save()

        return {"orderId": order}

    def list(self, request, auth):
        # принимаем только запросы методом POST
        if request.method != 'GET':
            raise Exception('error HTTP method')

        today_min = datetime.combine(date.today(), time.min)
        today_max = datetime.combine(date.today(), time.max)
        statuslist = list([Status.IN_PROGRESS, Status.READY, Status.NEW])
        orders = Order.objects.filter(
            point=auth[0].point, status__in=statuslist, created_at__range=(today_min, today_max))
        if orders.exists():
            result = list()
            for raw in orders:
                result.append(raw.as_json())
            return {"orders": result}
        else:
            return {"orders": {}}
