from django.shortcuts import render
from django.template import Context
from .models import Location

# Create your views here.

def map(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    location = Context({"lat":float(lat), "lng":float(lng)})
    return render(request,'map/map.html',{'location': location})

def curmap(request,lat,lng):
    location = Context({"lat":float(lat), "lng":float(lng)})

    # if len(location) > 0:
    #     loc = location[0]
    # else:
    #     loc = None

    return render(request, 'map/map.html', {'location': location})