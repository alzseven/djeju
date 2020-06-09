from django.contrib.gis.db import models as models

# Create your models here.
class Sido(models.Model):
    seq = models.IntegerField() #번호
    create_dt = models.CharField(max_length=30) #등록일시분초
    death_cnt = models.IntegerField() #사망자 수
    defCnt = models.IntegerField() #합계
    gubun = models.CharField(max_length=30,primary_key=True) #시도명(한글)
    gubun_cn = models.CharField(max_length=30) #시도명(중국어)
    gubun_en = models.CharField(max_length=30) #시도명(영어)
    inc_dec = models.IntegerField() #전일대비 증감수
    isol_clear_cnt = models.IntegerField() #격리 해제 수
    isollingCnt = models.IntegerField() #격리해제
    localOccCnt = models.IntegerField() #격리중
    overFlowCnt = models.IntegerField() #해외유입(잠정)
    qur_rate = models.CharField(max_length=30) #10만명당 발생률
    std_day = models.CharField(max_length=30) #기준일시

    def __str__(self):
        return self.gubun
