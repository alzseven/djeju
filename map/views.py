from django.shortcuts import render
from django.template import Context
import json
import requests
from map.models import Hospitals
from django.http import HttpResponse

from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.db.models import Subquery
from django.core import serializers

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

def maskmap(request):
    # djangoReq
    cur_lat = request.GET.get('lat')
    cur_lng = request.GET.get('lng')
    lvl = int(request.GET.get("level"))

    dis = 0
    if(lvl>0 and lvl<5):
        dis = 125 * 2**(lvl+1)
    elif(lvl>=5):
        dis = 5000
    # else:
    #     #invalid value
    #     dis = 0

    apiReqtxt = "lat="+ str(cur_lat) + "&lng=" + str(cur_lng) + "&m=" + str(dis) 
    url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json?" + apiReqtxt
    result = requests.get(url).text
   
    data = Context(
        {"lat":float(cur_lat),
         "lng":float(cur_lng),
         "lvl":int(lvl),
         "strdata":str(result)
         })

    #TODO:Filtering at view?
    return render(request, 'map/maskstore.html', {'strdata':data})

def hospmap(request):
    cur_lat = request.GET.get('lat')
    cur_lng = request.GET.get('lng')
    lvl = int(request.GET.get("level"))

    dis = 0
    if(lvl>0 and lvl<5):
        dis = 125 * 2**(lvl+1)
    elif(lvl>=5):
        dis = 5000 #TODO:Set New Max
    # else:
    #     #invalid value
    #     dis = 0

    user_location = fromstr(f'POINT({float(cur_lng)} {float(cur_lat)})', srid=4326)

    # context_object_name = "shops"
    # queryset = Hospitals.objects.filter(float(Distance("location",user_location).m)< dis) #어짜피 안에 있는거 다 꺼내면 좌표 기반으로 찍힘
    # queryset = Hospitals.objects.annotate(distance=Distance("location", user_location)).filter(distance__m <= dis)
    qs = Hospitals.objects.filter(location__distance_lte=(user_location, dis)).values('latitude','longtitude','yadmNm','hospTyTpCd','telno','adtFrDd','spclAdmTyCd')

    # qs = queryset.filter(distance.m < dis).order_by("distance") #.filter(distance).order_by("distance")[0:3]
    # qs = list(filter(lambda hospitals,values: hospitals.distance.m <= dis), list(queryset))

    # q = Hospitals.objects.filter(places__point__distance_lte=(point, D(mi=distance_miles_to_search))).annotate(closest_city_id=F('places__city'))

    # point = Point(float(longitude), float(latitude), srid=4326)
    # buffered = point.buffer(buffer_width)  

    # queryset = queryset.filter(coordinates__within=user_location.buffer(buff))  
    # queryset = queryset.annotate(distance=Distance('coordinates', point))  

    # qs = Hospitals.objects.annotate(
    #     distance = Distance("location",user_location)) Subquery(
    #         )
    #     Distance
    #     Subquery(.m < dis)
    # ).order_by("distance")

    # for d in queryset:
    #     print(d.distance.m)
    #     print(type(d.distance.m))
    #print(str(queryset.values()))

    #hos_list = serializers.serialize('json', qs)

    data = Context(
        {"lat":float(cur_lat),
         "lng":float(cur_lng),
         "lvl":int(lvl),
         "hosdata":json.dumps(list(qs), ensure_ascii=False, default=str)
         })

    #TODO:Filtering at view?

    #return HttpResponse(json.dumps(list(qs), ensure_ascii=False, default=str))
    return render(request, 'map/hospital.html', {'data':data})

# def infstate(request):
#     return Null
