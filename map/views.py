from django.shortcuts import render
from .models import Location

# Create your views here.

def map(request):
    return render(request,'map/map.html',{})

def curmap(request,lat,lng):
    location = Location.objects.filter(lat=float(lat), lng=float(lng))
    return render(request, 'map/map.html', {'loc': location})