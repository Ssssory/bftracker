
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .helper.logic import Logic

HTTP_200 = 200
HTTP_401 = 401
HTTP_400 = 400


@csrf_exempt
def auth(request):
    logic = Logic()
    try:
        result = logic.auth(request)
        return JsonResponse(result, status=HTTP_200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_400)


@csrf_exempt
def order(request):
    logic = Logic()
    # отдельно обрабатываем токен, чтобы отдать 401 при его протухании
    try:
        auth = logic.getHeaderAuth(request)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_401)
    
    try:
        result = logic.order(request,auth)
        return JsonResponse(result, status=HTTP_200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_400)


@csrf_exempt
def link(request):
    logic = Logic()
    # отдельно обрабатываем токен, чтобы отдать 401 при его протухании
    try:
        auth = logic.getHeaderAuth(request)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_401)

    try:
        result = logic.link(request, auth)
        return JsonResponse(result, status=HTTP_200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_400)

@csrf_exempt
def status(request):
    logic = Logic()
    # отдельно обрабатываем токен, чтобы отдать 401 при его протухании
    try:
        auth = logic.getHeaderAuth(request)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_401)

    try:
        result = logic.status(request, auth)
        return JsonResponse(result, status=HTTP_200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_400)


@csrf_exempt
def list(request):
    logic = Logic()
    # отдельно обрабатываем токен, чтобы отдать 401 при его протухании
    try:
        auth = logic.getHeaderAuth(request)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_401)

    try:
        result = logic.list(request, auth)
        return JsonResponse(result, status=HTTP_200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_400)
