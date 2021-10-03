from .models import Client, Order, Point, Restaurant
from .forms import PointForm
from django.shortcuts import render

# Create your views here.


def test(request):
    return render(request,'pages/test.html')

def index(request):
    return render(request,'pages/landing.html')

def dashboard(request):
    rests = Restaurant.objects.all()
    points = Point.objects.all()
    orders = Order.objects.count()
    clients = Client.objects.count()
    return render(request, 'pages/dashboard.html', 
    {"rests":rests,"points":points,"orders":orders,"clients":clients})



def points(request):
    if request.method == 'POST':
        pass
    else:
        form = PointForm()
    return render(request, 'pages/points.html', {"form":form})
def config(request):
    return render(request, 'pages/config.html')


def admin_dashboard(request):
    rests = Restaurant.objects.all()
    return render(request, 'pages/admin/restorants.html',
                  {"rests": rests})


def admin_dashboard_point_stat(request, owner, point):
    rest = Restaurant.objects.get(pk=owner)
    if rest:
        order = Order.objects.filter(point=point)
        return render(request, 'pages/admin/point.html',
                      {"order": order})
    else:
        raise Exception('Restaurant id error')
