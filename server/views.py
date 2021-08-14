from .models import Client, Order, Point, Restaurant
from .forms import PointForm
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def test(request):
    return render(request,'pages/test.html')

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
