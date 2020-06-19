from django.core.management.base import BaseCommand, CommandError
import requests
import xmltodict
from info.models import Sido
from django.utils import timezone
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour='10-18', minute=0)
def scheduled_job():
    now = timezone.localtime()
    day_str = (str(now.day)) if now.day > 9 else ("0" + str(now.day))
    month_str = (str(now.month)) if now.month > 9 else ("0" + str(now.month))
    today_str = str(now.year) + month_str + day_str

    key = "j%2BnuUay451ipAStppt2Uh7XE3aAUvC%2FtxdLMMHEreI7KR%2FY0%2B0%2BIAsODyasKyftwZXHwQ8SNTxD2QY5y2W8aXw%3D%3D"
    sidoUrl = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson" # + queryParams

    api_key_decode = requests.utils.unquote(key) 
    parameters = {"serviceKey":api_key_decode, "numOfROws":50, "pageNo":1, "startCreateDt":today_str, "endCreateDt":today_str}
    print(parameters)
    sidoReq = requests.get(sidoUrl, params = parameters).content
    sidoxmlObj = xmltodict.parse(sidoReq)

    isValidReq = False
    for i in range(0,11):
        if sidoxmlObj['response']['header']['resultCode'] == '00':
            isValidReq = True
            break
        sidoReq = requests.get(sidoUrl, params = parameters).content
        sidoxmlObj = xmltodict.parse(sidoReq)
    if not isValidReq:
        print("Sido: Invalid Request")
    else:
        if not sidoxmlObj['response']['body']['items']: 
            print("Sido : No Data Found")
        else:
            sidoData = sidoxmlObj['response']['body']['items']['item']            
            for i in range(len(sidoData)):
                Sido(seq = sidoData[i]['seq'],
                    create_dt = sidoData[i]['createDt'],
                    death_cnt = int(sidoData[i]['deathCnt']),
                    defCnt = int(sidoData[i]['defCnt']),
                    gubun = sidoData[i]['gubun'],
                    gubun_cn = sidoData[i]['gubunCn'],
                    gubun_en = sidoData[i]['gubunEn'],
                    inc_dec = int(sidoData[i]['incDec']),
                    isol_clear_cnt = int(sidoData[i]['isolClearCnt']),
                    isollingCnt = int(sidoData[i]['isolIngCnt']),
                    localOccCnt = int(sidoData[i]['localOccCnt']),
                    overFlowCnt = int(sidoData[i]['overFlowCnt']),
                    qur_rate = sidoData[i]['qurRate'],
                    std_day = sidoData[i]['stdDay'],
                    ).save()



class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Update Start!")
        sched.start()
