from django.template import Context
from django.shortcuts import render
import json
import requests
from django.http import JsonResponse
from info.models import Sido

def sidoview(request):
    # djangoReq
    cur_lat = request.GET.get('lat')
    cur_lng = request.GET.get('lng')
    #cur_dat = request.GET.get('dt')

    #TODO: request current_gubun with lat and lng 
    url = 'https://dapi.kakao.com/v2/local/geo/coord2address.json?'+ 'x=' + str(cur_lng) + '&y=' + str(cur_lat) + '&input_coord=WGS84'
    headers = {"Authorization": "KakaoAK a2c80bf54c05154661e3f99e258519a6" }
    result = json.loads(str(requests.get(url,headers=headers).text))
    cur_sido = result['documents'][0]['address']["region_1depth_name"] #?


    qs = Sido.objects.filter(gubun=cur_sido)

    


    # data = Context(
    #     {"lat":float(cur_lat),
    #      "lng":float(cur_lng),
    #      "dat":int(dt),
    #      "sidodata": json.dumps(list(qs))
    #     })

    #TODO:Filtering at view?
    #return render(request, 'map/maskstore.html', {'strdata':data})
    return JsonResponse(qs.values(), safe=False)