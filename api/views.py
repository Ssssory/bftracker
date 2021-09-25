import json
import collections
from server.classes.status import Status
from api.models import ApiTimeToken
from server.models import Order, Point, Restaurant
from django.http import JsonResponse
from .helper.answer import Answer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import MD5PasswordHasher
from django.conf import settings
from django.core import serializers

from uuid import uuid4
from django.utils import timezone
from datetime import date, datetime, time, timedelta


@csrf_exempt
def run(request):
    # принимаем только запросы методом POST
    if request.method != 'POST':
        return JsonResponse(Answer.error("error HTTP method", 0))
    # разбираем json в []
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # проверяем, что все необходимые ключи присутствуют в запросе
    reqKeys = ['jsonrpc', 'method', 'params', 'id']
    if collections.Counter(reqKeys) != collections.Counter(body.keys()):
        return JsonResponse(Answer.error("all fields required", 0))
    # дефолтный статус и текст ошибки. Переопределяются, если будет найден API метод
    status = "error"
    errorText = "no available method"
    # Первый уровень ключей в запросе
    id = body['id']
    reqMethod = body['method']
    params = body['params']

    dictStatuses = Status()

    # Публичные методы, закрываем авторизацией по токену
    if reqMethod == "auth":
        # {"jsonrpc": "2.0", "method": "auth", "params": {“login”: ”kasa1”, “password”: ”123456”}, "id": 1}
        # {"jsonrpc": "2.0", "result": {“status”: ”success”, “data”: {“token”: ”94a08da1fecbb6e8b46990538c7b50b2”}}, "id": 1}
        login = params['login']
        password = params['password']

        point = Point.objects.get(login=login)
        #print(point.as_json())
        try:
            # проверяем корректность пароля
            if point.password == MD5PasswordHasher().encode(
                    str(password), settings.SALT):
                token = ApiTimeToken.getOrCreateToken(point)
                status = "success"
                resp = {"token": token, "point": point.as_json()}
            else:
               errorText = "incorrect login or password"
        except:
            errorText = "incorrect login or password"

    if reqMethod == "order":
        order = params['order']
        token = params['token']

        auth = ApiTimeToken.objects.filter(token=token)
        if auth.exists():
            newOrder = Order(
                order_id=order,
                client=None,
                point=auth[0].point,
                status=Status.NEW
            )
            newOrder.save()
            status = "success"
            resp = {"order": newOrder.as_json()}
        else:
            errorText = "incorrect login or password"

    if reqMethod == "status":
        token = params['token']
        auth = ApiTimeToken.objects.filter(token=token)
        if auth.exists():
            orderId = params['orderId']
            status = params['status']
            order = Order.objects.get(order_id=orderId)
            try:
                order.status = status
                order.save()
                status = "success"
                resp = {"orderId": orderId}
            except:
                errorText = "can not update order"
        else:
            errorText = "incorrect token"
    
    if reqMethod == "list":
        token = params['token']
        auth = ApiTimeToken.objects.filter(token=token)
        if auth.exists():
            today_min = datetime.combine(date.today(), time.min)
            today_max = datetime.combine(date.today(), time.max)
            statuslist = list([Status.IN_PROGRESS, Status.READY, Status.NEW])
            orders = Order.objects.filter(
                point=auth[0].point, status__in=statuslist, created_at__range=(today_min, today_max)) 
            if orders.exists():
                result = list()
                for raw in orders:
                    result.append(raw.as_json())
                resp = {"orders": result}
            else:
                resp = {"orders": {}}

            status = "success"
        else:
            errorText = "incorrect token"
    
    if reqMethod == "dictionary":
        token = params['token']
        auth = ApiTimeToken.objects.filter(token=token)
        if auth.exists():
            status = "success"
            resp = {"statuses": dictStatuses.as_json()}
        else:
            errorText = "incorrect token"
        
    if reqMethod == "link":
        token = params['token']
        auth = ApiTimeToken.objects.filter(token=token)
        if auth.exists():
            point = auth[0].point
            link = "t.me/ZhduEduBot"
            status = "success"
            resp = {"link": link, "point": point.as_json()}
        else:
            errorText = "incorrect token"
        
    
    #  Служебные роуты. Отключить после деплоя.
    if reqMethod == "newRestaurant":

        newRest = Restaurant(
            login=params['login'],
            password=MD5PasswordHasher().encode(
                str(params['password']), settings.SALT),
            name=params['name']
            )
        newRest.save()
        status = "success"
        resp = [newRest.as_json()]

    if reqMethod == "newPoint":
        rest = Restaurant.objects.get(id=params['restaurant'])
        newPoint = Point(
            restaurant=rest,
            login=params['login'],
            password=MD5PasswordHasher().encode(
                str(params['password']), settings.SALT),
            name=params['name']
            )
        newPoint.save()
        status = "success"
        resp = [newPoint.as_json()]

    if reqMethod == "password":
        # password=params['password'],
        # password = MD5PasswordHasher().encode(str(password),'123')
        # status = "success"
        # resp = password
        rest = Restaurant.objects.get(id=1)
        status = "success"
        # resp = serializers.serialize('json', [rest])
        if type(rest) in (tuple, list):
            resp = [ob.as_json() for ob in rest]
        else:    
            resp = [rest.as_json()]
        print(type(rest) == "Restaurant")

        pass


    # print(body.keys())

    if status == "success":
        return JsonResponse(Answer.success(resp, id))
    else:
        return JsonResponse(Answer.error(errorText, id))