from django.shortcuts import render
from .models import Location

# Create your views here.

def map(request):
    return render(request,'map/map.html',{})

def curmap(request,lat,lng):
    location = {lat:float(lat), lng:float(lng)}

    # if len(location) > 0:
    #     loc = location[0]
    # else:
    #     loc = None

    return render(request, 'map/map.html', {'location': location})