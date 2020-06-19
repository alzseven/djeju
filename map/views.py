from django.shortcuts import render
from django.template import Context
import json
import requests
from map.models import Hospitals
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance


# Create your views here.

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

    return render(request, 'map/maskstore.html', {'strdata':data})

def hospmap(request):
    cur_lat = request.GET.get('lat')
    cur_lng = request.GET.get('lng')
    lvl = int(request.GET.get("level"))

    dis = 0
    if(lvl>0 and lvl<5):
        dis = 250 * 2**(lvl+1)
    elif(lvl>=5):
        dis = 10000 #TODO:Set New Max
    # else:
    #     #invalid value
    #     dis = 0

    user_location = fromstr(f'POINT({float(cur_lng)} {float(cur_lat)})', srid=4326)

    qs = Hospitals.objects.filter(location__distance_lte=(user_location, dis))\
        .values('latitude','longtitude','yadmNm','hospTyTpCd','telno','adtFrDd','isReliefhos','isInspect','isTriage')

    data = Context(
        {"lat":float(cur_lat),
         "lng":float(cur_lng),
         "lvl":int(lvl),
         "hosdata":json.dumps(list(qs), ensure_ascii=False, default=str)
         })

    #TODO:Filtering at view?

    return render(request, 'map/hospital.html', {'data':data})
