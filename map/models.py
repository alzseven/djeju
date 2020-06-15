from django.contrib.gis.db import models as gismodels

class Hospitals(gismodels.Model):
    latitude = gismodels.FloatField()
    longtitude = gismodels.FloatField()
    sidoNm = gismodels.CharField(max_length=400)      #시도명
    sgguNm = gismodels.CharField(max_length=400)      #시군구명
    location = gismodels.PointField()
    yadmNm = gismodels.CharField(max_length=200)      #기관명 = 병원이름
    hospTyTpCd = gismodels.CharField(max_length=2,null=True,blank=True)  #선정유형 = 국민안심병원 선정유형
    isReliefhos = gismodels.BooleanField() 
    isInspect = gismodels.BooleanField()
    isTriage = gismodels.BooleanField()
    telno = gismodels.CharField(max_length=30,primary_key=True)       #전화번호
    adtFrDd = gismodels.CharField(max_length=8)     #운영가능일자
    # spclAdmTyCd = gismodels.CharField(max_length=2) #구분코드

    def __str__(self):
         return self.yadmNm
