from django.shortcuts import render
from django.template import Context
import json
import requests
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

def maskmap(request):
    # djangoReq
    cur_lat = request.GET.get('lat')
    cur_lng = request.GET.get('lng')
    lvl = request.GET.get("level")
    # dis = request.GET.get('dis')

    dis = 0
    if(lvl>0 and lvl<3):
        dis = 50
    elif(lvl>=3 and lvl<=9):
        dis = 75 * 2**(lvl-3)
    else:
        #invalid value
        dis = 0

    apiReqtxt = "lat="+str(cur_lat) + "&lng=" + str(cur_lng) + "&m=" + str(dis) 
    # apiReq
    url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json?" + apiReqtxt
    req = requests.get(url)
    #total_page = req.json()['totalPages'] 
    # count = req.json()['count']
    # stores = req.json()['stores']

    # addrs = []
    # #codes = []
    # #cres = []
    # lats = [] 
    # lngs = [] 
    # names = []
    # stats = []
    # stks = []
    # types = []

    # for i in range(len(stores)):
    #     addrs.append(stores[i]['addr'])
    # #    codes.append(stroes[i]['code'])
    # #    cres.append(stroes[i]['created_at'])
    #     lats.append(stores[i]['lat'])
    #     lngs.append(stores[i]['lng'])
    #     names.append(stores[i]['name'])
    #     stats.append(stores[i]['remain_stat'])
    #     stks.append(stores[i]['stock_at'])
    #     types.append(stores[i]['type'])
    
    data = Context(
        {"lat":float(cur_lat),
         "lng":float(cur_lng),
         "lvl":int(lvl),
         "strdata":str(req)
        #  "str_addr":list(addrs),
        #  #"str_code":list(codes),
        #  #"str_cre":list(cres),
        #  "str_lat":list(lats),
        #  "str_lng":list(lngs),
        #  "str_name":list(names),
        #  "str_stat":list(stats),
        #  "str_stk":list(stks),
        #  "str_type":list(types),
         })

    return render(request, 'map/maskstore.html', {'data':data})