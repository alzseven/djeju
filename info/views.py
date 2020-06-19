from django.template import Context
from django.shortcuts import render
import json
import requests
from django.http import JsonResponse
from info.models import Sido
from django.core import serializers

def sidoview(request):
    cur_lat = request.GET.get('lat')
    cur_lng = request.GET.get('lng')

    url = 'https://dapi.kakao.com/v2/local/geo/coord2address.json?'+ 'x=' + str(cur_lng) + '&y=' + str(cur_lat) + '&input_coord=WGS84'
    headers = {"Authorization": "KakaoAK a2c80bf54c05154661e3f99e258519a6" }
    result = json.loads(str(requests.get(url,headers=headers).text))
    cur_sido = result['documents'][0]['address']["region_1depth_name"][0:2]

    queryset = Sido.objects.filter(gubun__contains=cur_sido)
    values = list(queryset.values("gubun","defCnt","isol_clear_cnt","death_cnt","std_day"))

    data = {
            "keys":["시도명","확진","격리해제","사망","기준일시"],
            "시도명": values[0]["gubun"],
            "확진": values[0]["defCnt"],
            "격리해제": values[0]["isol_clear_cnt"],
            "사망": values[0]["death_cnt"],
            "기준일시": values[0]["std_day"]
        }
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii':False})

def appinfo(request):
    d = [{'funcName':"공적 마스크 판매처",
        'ViewType': "WebView",
        'requirements': "none",
        'reqUrl': "https://injejuweb.herokuapp.com/map/maskstore"},
        {'funcName':"코로나-19관련 병원정보",
        'ViewType': "WebView",
        'requirements': "none",
        'reqUrl':"https://injejuweb.herokuapp.com/map/reliefhospitals"},
        {'funcName':"시도별 감염 현황",
        'ViewType': "ListView",
        'requirements': "location",
        'reqUrl': "http://injejuweb.herokuapp.com/info/sido"}        
        ]
    
    return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii':False})