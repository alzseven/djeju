import sys
import requests
import xmltodict
from django.contrib.gis.geos import fromstr
from map.models import Hospitals

def run():
    CREATE_CODE = 1
    # READ_CODE = 2
    # UPDATE_CODE = 3
    DELETE_CODE = 4
    RESET_CODE = 5

    args = int(input("번호 입력:"))
    if (args==CREATE_CODE):
        num = int(input("구분코드의 번호를 입력해주세요.\n1. 국민안심병원\n2. 코로나 검사 실시기관\n3. 코로나 선별진료소 운영기관\n"))
        if(num==1):
            createhos("A0")
        elif(num==2):
            createhos("97")
        elif(num==3):
            createhos("99")
        else:
            print("Invalid input")
    # elif (args==2):
    #     pass
    # elif (args==3):
    #     pass
    elif (args==DELETE_CODE):
        pass
    elif (args==RESET_CODE):
        Hospitals.objects.all().delete()
        print("Reset Done")
    else:
        print("Invalid input")

def createhos(hosType):
    numOfRows = 100
    key = "uQQjZyj3ItqNMxCFKiX5%2BE4KhvWalHJc0vVjBDUpmvM7Z%2Bb3ZBBrN1ZVuwyZ7sO0SeJCTVRnS5N7wxZq1ok%2FaA%3D%3D"
    preUrl = "http://apis.data.go.kr/B551182/pubReliefHospService/getpubReliefHospList?ServiceKey=" + key + "&pageNo=1&numOfRows=10&spclAdmTyCd=" + hosType
    preReq = requests.get(preUrl).content
    prexmlObj = xmltodict.parse(preReq)
    totalCount = prexmlObj['response']['body']['totalCount']

    _sidoNm = ""
    _sgguNm = ""
    _lat = 0.0
    _lng = 0.0
    _yadmNm = ""
    _hospTyTpCd = ""
    _telno = ""
    _adtFrDd = ""
    _spclAdmTyCd = ""

    for page_num in range(1,(int(totalCount)//numOfRows)+2):
        relihosUrl = "http://apis.data.go.kr/B551182/pubReliefHospService/getpubReliefHospList?ServiceKey=" + key +"&pageNo=" + str(page_num) + "&numOfRows=" + str(numOfRows) + "&spclAdmTyCd=" + hosType
        reliReq = requests.get(relihosUrl).content
        relixmlObj = xmltodict.parse(reliReq)
        reliData = relixmlObj['response']['body']['items']['item']
        
        for i in range(len(reliData)):
            hos_name = reliData[i]['yadmNm'].replace(' ','%20')
            basehosUrl = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?ServiceKey=' + key +'&yadmNm=' + hos_name +"&numOfRows=50"
            basehosReq = requests.get(basehosUrl).content
            basehosxmlObj = xmltodict.parse(basehosReq)
            if not basehosxmlObj['response']['body']['items']: 
                print(hos_name + ": No Data Found")
                continue
            else:
                basehosdata = basehosxmlObj['response']['body']['items']['item'] 
            basehosCount = int(basehosxmlObj['response']['body']['totalCount'])

            if basehosCount > 1:
                flag = True
                for i2 in range(len(basehosdata)):
                    if basehosdata[i2]['telno'].replace('-','') == reliData[i]['telno'].replace('-',''): #시도명 시군구명 데이터 멋대로라 대조 불가
                        _lat = float(basehosdata[i2]['YPos'])
                        _lng = float(basehosdata[i2]['XPos'])
                        flag = False
                        break
                if flag == True:
                    print("Error: No Data Matches")
                    sys.exit(1)
            elif basehosCount == 1:
                if basehosdata:
                    _lat = float(basehosdata['YPos'])
                    _lng = float(basehosdata['XPos'])
                else:
                    print("Error: Failed To Get Response")
                    sys.exit(1)
            else:
                print("Error: No Data Found")
                sys.exit(1)

            _sidoNm = reliData[i]['sidoNm']
            _sgguNm = reliData[i]['sgguNm']
            _yadmNm = reliData[i]['yadmNm']
            if 'hospTyTpCd' in reliData[i].keys():
                _hospTyTpCd = reliData[i]['hospTyTpCd']
            _telno = reliData[i]['telno']
            _adtFrDd = reliData[i]['adtFrDd']
            _spclAdmTyCd = reliData[i]['spclAdmTyCd']

            Hospitals(  latitude = _lat,
                        longtitude = _lng,
                        sidoNm = _sidoNm,
                        sgguNm = _sgguNm,
                        location = fromstr(f'POINT({float(_lng)} {float(_lat)})', srid=4326),
                        yadmNm = _yadmNm,
                        hospTyTpCd = _hospTyTpCd,
                        telno = _telno,
                        adtFrDd = _adtFrDd,
                        spclAdmTyCd = _spclAdmTyCd,).save()