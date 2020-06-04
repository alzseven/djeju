from django.contrib.gis.geos import fromstr
from map.models import Hospitals

def run(args):
    CREATE_CODE = 1
    READ_CODE = 2
    UPDATE_CODE = 3
    DELETE_CODE = 4
    RESET_CODE = 5

    if (args==1):
        pass
    elif (args==2):
        pass
    elif (args==3):
        pass
    elif (args==4):
        pass
    elif (args==5):
        Hospitals.objects.all().delete()
    else:
        pass

def createdata(_lat,_lng,_sidoNm,_sgguNm,_yadmNm,_hospTyTpCd,_telno,_spclAdmTyCd):
    Hospitals(  latitude = _lat,
                        longtitude = _lng,
                        sidoNm = _sidoNm,
                        sgguNm = _sgguNm,
                        location = fromstr(f'POINT({float(_lng)} {float(_lat)})', srid=4326),
                        yadmNm = _yadmNm,
                        hospTyTpCd = _hospTyTpCd,
                        telno = _telno,
                        spclAdmTyCd = _spclAdmTyCd,).save()