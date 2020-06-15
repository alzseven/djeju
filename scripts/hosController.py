import sys
import requests
import xmltodict
from django.contrib.gis.geos import fromstr
from map.models import Hospitals

# TODO:데이터 시작위치, 끝 위치 받아서 가져오게 해야함
def run():
    CREATE_CODE = 1
    # READ_CODE = 2
    # UPDATE_CODE = 3
    DELETE_CODE = 4
    RESET_CODE = 5

    args = int(input("번호 입력:"))
    if (args==CREATE_CODE):
        createhos()
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

def createhos():
    numOfRows = 100
    key = "j%2BnuUay451ipAStppt2Uh7XE3aAUvC%2FtxdLMMHEreI7KR%2FY0%2B0%2BIAsODyasKyftwZXHwQ8SNTxD2QY5y2W8aXw%3D%3D"
    preUrl = "http://apis.data.go.kr/B551182/pubReliefHospService/getpubReliefHospList?ServiceKey=" + key + "&pageNo=1&numOfRows=10"
    preReq = requests.get(preUrl).content
    prexmlObj = xmltodict.parse(preReq)
    totalCount = prexmlObj['response']['body']['totalCount']

    # _spclAdmTyCd = ""

    print("총 데이터 수: " + totalCount)
    input_min = int(input("입력을 시작할 페이지: (페이지 당 데이터 100개"))
    input_max = int(input("입력을 종료할 페이지: (페이지 당 데이터 100개"))
    if(input_max >= (int(totalCount)//numOfRows) + 1 or input_min < 1):
        print("잘못된 입력입니다.")
        sys.exit(1)

    # 1,(int(totalCount)//numOfRows)+2
    for page_num in range(input_min, input_max):
        _sidoNm = ""
        _sgguNm = ""
        _lat = 0.0
        _lng = 0.0
        _yadmNm = ""
        _hospTyTpCd = ""
        _isReliefhos = False
        _isInspect = False
        _isTriage = False
        _telno = ""
        _adtFrDd = ""


        relihosUrl = "http://apis.data.go.kr/B551182/pubReliefHospService/getpubReliefHospList?ServiceKey=" \
            + key +"&pageNo=" + str(page_num) + "&numOfRows=" + str(numOfRows)
        reliReq = requests.get(relihosUrl).content
        relixmlObj = xmltodict.parse(reliReq)
        reliData = relixmlObj['response']['body']['items']['item']
        
        _sidoNm = reliData[i]['sidoNm']
        _sgguNm = reliData[i]['sgguNm']
        _yadmNm = reliData[i]['yadmNm']
        if 'hospTyTpCd' in reliData[i].keys():
            _hospTyTpCd = reliData[i]['hospTyTpCd']
        _adtFrDd = reliData[i]['adtFrDd']
        _telno = reliData[i]['telno']
        
        # if reliData[i]['spclAdmTyCd']
        if Hospitals.object.filter(telno = _telno).exists():
            if reliData[i]['spclAdmTyCd'] == "A0":
                Hospitals.object.filter(telno = _telno).update(isReliefhos = True)
                continue
            elif reliData[i]['spclAdmTyCd'] == "97":
                Hospitals.object.filter(telno = _telno).update(isInspect = True)
                continue
            elif reliData[i]['spclAdmTyCd'] == "99":
                Hospitals.object.filter(telno = _telno).update(isTriage = True)
                continue
        # _spclAdmTyCd = reliData[i]['spclAdmTyCd']    
        else:
            if reliData[i]['spclAdmTyCd'] == "A0":
                _isReliefhos = True
            elif reliData[i]['spclAdmTyCd'] == "97":
                _isInspect = True
            elif reliData[i]['spclAdmTyCd'] == "99":
                _isTriage = True
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

                Hospitals(  latitude = _lat,
                            longtitude = _lng,
                            sidoNm = _sidoNm,
                            sgguNm = _sgguNm,
                            location = fromstr(f'POINT({float(_lng)} {float(_lat)})', srid=4326),
                            yadmNm = _yadmNm,
                            hospTyTpCd = _hospTyTpCd,
                            isReliefhos = _isReliefhos,
                            isInspect = _isInspect,
                            isTriage = _isTriage,
                            telno = _telno,
                            adtFrDd = _adtFrDd,).save()
                            #spclAdmTyCd = _spclAdmTyCd,