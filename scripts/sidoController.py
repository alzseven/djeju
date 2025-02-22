import sys
import requests
import xmltodict
from info.models import Sido
from django.utils import timezone

def run():
    CREATE_CODE = 1
    # READ_CODE = 2
    # UPDATE_CODE = 3
    DELETE_CODE = 4
    RESET_CODE = 5

    args = int(input("번호 입력:"))
    if (args==CREATE_CODE):
        createsido()
    # elif (args==2):
    #     pass
    # elif (args==3):
    #     pass
    elif (args==DELETE_CODE):
        pass
    elif (args==RESET_CODE):
        Sido.objects.all().delete()
        print("Reset Done")
    else:
        print("Invalid input")

def createsido():

    _seq = 0
    _createdt = ""
    _deathcnt = 0
    _defCnt = 0
    _gubun = ""
    _gubuncn = ""
    _gubunen = ""
    _incdec = 0
    _isolclearcnt = 0
    _isollingCnt = 0
    _localOccCnt = 0
    _overFlowCnt = 0
    _qurrate = ""
    _stdday = ""

    now = timezone.localtime()
    day_str = (str(now.day)) if now.day > 9 else ("0" + str(now.day))
    month_str = (str(now.month)) if now.month > 9 else ("0" + str(now.month))
    today_str = str(now.year) + month_str + day_str

    key = "j%2BnuUay451ipAStppt2Uh7XE3aAUvC%2FtxdLMMHEreI7KR%2FY0%2B0%2BIAsODyasKyftwZXHwQ8SNTxD2QY5y2W8aXw%3D%3D"

    sidoUrl = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson" # + queryParams

    api_key_decode = requests.utils.unquote(key) 
    parameters = {"serviceKey":api_key_decode, "numOfROws":50, "pageNo":1, "startCreateDt":today_str, "endCreateDt":today_str}
    sidoReq = requests.get(sidoUrl, params = parameters).content

    sidoxmlObj = xmltodict.parse(sidoReq)
    print("key: " + key)
    print(sidoxmlObj)
    if not sidoxmlObj['response']['body']['items']: 
        print("Sido : No Data Found")
        sys.exit(1)
    else:
        sidoData = sidoxmlObj['response']['body']['items']['item']
        
        for i in range(len(sidoData)):

            _seq = sidoData[i]['seq']
            _createdt = sidoData[i]['createDt']
            _deathcnt = int(sidoData[i]['deathCnt'])
            _defCnt = int(sidoData[i]['defCnt'])
            _gubun = sidoData[i]['gubun']
            _gubun_cn = sidoData[i]['gubunCn']
            _gubun_en = sidoData[i]['gubunEn']
            _inc_dec = int(sidoData[i]['incDec'])
            _isol_clear_cnt = int(sidoData[i]['isolClearCnt'])
            _isollingCnt = int(sidoData[i]['isolIngCnt'])
            _localOccCnt = int(sidoData[i]['localOccCnt'])
            _overFlowCnt = int(sidoData[i]['overFlowCnt'])
            _qurrate = sidoData[i]['qurRate']
            _stdday = sidoData[i]['stdDay']

            Sido(seq = _seq,
                create_dt = _createdt,
                death_cnt = _deathcnt,
                defCnt = _defCnt,
                gubun = _gubun,
                gubun_cn = _gubun_cn,
                gubun_en = _gubun_en,
                inc_dec = _inc_dec,
                isol_clear_cnt = _isol_clear_cnt,
                isollingCnt = _isollingCnt,
                localOccCnt = _localOccCnt,
                overFlowCnt = _overFlowCnt,
                qur_rate = _qurrate,
                std_day = _stdday,
                ).save()