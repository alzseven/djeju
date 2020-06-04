from django.conf import settings
from django.contrib.gis.db import models as gismodels

#from django.utils import timezone


# class MaskStores(models.Model):
#     addr = models.CharField(max_length = 200)
#     code = models.IntegerField()
#     lat = models.FloatField()
#     lng = models.FloatField()
#     name = models.CharField(max_length = 200)

class Hospitals(gismodels.Model):
    latitude = gismodels.FloatField()
    longtitude = gismodels.FloatField()
    sidoNm = gismodels.CharField(max_length=400)      #시도명
    sgguNm = gismodels.CharField(max_length=400)      #시군구명
    location = gismodels.PointField()
    yadmNm = gismodels.CharField(max_length=200)      #기관명 = 병원이름
    hospTyTpCd = gismodels.CharField(max_length=2,null=True,blank=True)  #선정유형 = 국민안심병원 선정유형
    telno = gismodels.CharField(max_length=30,primary_key=True)       #전화번호
    adtFrDd = gismodels.CharField(max_length=8)     #운영가능일자
    spclAdmTyCd = gismodels.CharField(max_length=2) #구분코드

    def __str__(self):
         return self.yadmNm

    #original post:

    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # title = models.CharField(max_length=200)
    # text = models.TextField()
    # created_date = models.DateTimeField(
    #         default=timezone.now)
    # published_date = models.DateTimeField(
    #         blank=True, null=True)

    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()

    # def __str__(self):
    #     return self.title