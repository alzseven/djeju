import sys
import requests
import xmltodict
from django.contrib.gis.geos import fromstr
from map.models import Hospitals

def run():

    Hospitals.objects.all().delete()

    numOfRows = 100
    key = "uQQjZyj3ItqNMxCFKiX5%2BE4KhvWalHJc0vVjBDUpmvM7Z%2Bb3ZBBrN1ZVuwyZ7sO0SeJCTVRnS5N7wxZq1ok%2FaA%3D%3D"
    preUrl = "http://apis.data.go.kr/B551182/pubReliefHospService/getpubReliefHospList?ServiceKey=" + key + "&pageNo=1&numOfRows=10"
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
        relihosUrl = "http://apis.data.go.kr/B551182/pubReliefHospService/getpubReliefHospList?ServiceKey=" + key +"&pageNo=" + str(page_num) + "&numOfRows=" + str(numOfRows)
        reliReq = requests.get(relihosUrl).content
        relixmlObj = xmltodict.parse(reliReq)
        reliData = relixmlObj['response']['body']['items']['item']
        
        for i in range(len(reliData)):
            hos_name = reliData[i]['yadmNm'].replace(' ','%20')
            basehosUrl = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?ServiceKey=' + key +'&yadmNm=' + hos_name +"&numOfRows=50"
            basehosReq = requests.get(basehosUrl).content
            basehosxmlObj = xmltodict.parse(basehosReq)
            if not basehosxmlObj['response']['body']['items']: 
                print(hos_name)
                continue
                #sys.exit(1)
            else:
                basehosdata = basehosxmlObj['response']['body']['items']['item'] 
            basehosCount = int(basehosxmlObj['response']['body']['totalCount'])

            if basehosCount > 1:
                flag = True
                for i2 in range(len(basehosdata)):
                    if basehosdata[i2]['telno'].replace('-','') == reliData[i]['telno'].replace('-',''): #시도명 시군구명 데이터 멋대로라 대조 불가
                        _lat = float(basehosdata[i2]['YPos'])
                        _lng = float(basehosdata[i2]['XPos'])
                        # lats.append(float(basehosdata[0]['YPos']))
                        # lngs.append(float(basehosdata[0]['XPos']))
                        flag = False
                        break
                if flag == True:
                    print("Error: No Data Matches")
                    sys.exit(1)
            elif basehosCount == 1:
                if basehosdata:
                    _lat = float(basehosdata['YPos'])
                    _lng = float(basehosdata['XPos'])
                    # lats.append(float(basehosdata['YPos']))
                    # lngs.append(float(basehosdata['XPos']))
                else:
                    print("Error: Failed To Get Response")
                    sys.exit(1)
            else:
                print("Error: No Data Found")
                sys.exit(1)


            # sidoNms.append(reliData[i]['sidoNm'])
            # sgguNms.append(reliData[i]['sgguNm'])
            # yadmNms.append(reliData[i]['yadmNm'])
            _sidoNm = reliData[i]['sidoNm']
            _sgguNm = reliData[i]['sgguNm']
            _yadmNm = reliData[i]['yadmNm']
            if 'hospTyTpCd' in reliData[i].keys():
                # hospTyTpCds.append(reliData[i]['hospTyTpCd'])
                _hospTyTpCd = reliData[i]['hospTyTpCd']
            # telnos.append(reliData[i]['telno'])
            # adtFrDds.append(reliData[i]['adtFrDd'])
            # spclAdmTyCds.append(reliData[i]['spclAdmTyCd'])
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

    # latitude = gismodels.FloatField()
    # longtitude = gismodels.FloatField()
    # sidoNm = gismodels.CharField(max_length=400)      #시도명
    # sgguNm = gismodels.CharField(max_length=400)      #시군구명
    # location = gismodels.PointField()
    # yadmNm = gismodels.CharField(max_length=200)      #기관명 = 병원이름
    # hospTyTpCd = gismodels.CharField(max_length=2)  #선정유형 = 국민안심병원 선정유형
    # telno = gismodels.CharField(max_length=30)       #전화번호
    # # adtFrDd = gismodels.CharField(max_length=8)     #운영가능일자
    # spclAdmTyCd = gismodels.CharField(max_length=2) #구분코드

## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
# if __name__=='__main__':
#     print("init")
#     crawlReliefHospitals()
#     blog_data_dict = parse_blog()
#     for t, l in blog_data_dict.items():
#         BlogData(title=t, link=l).save()

# class BlogData(models.Model):
#     title = models.CharField(max_length=200)
#     link = models.URLField()