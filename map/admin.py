from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Hospitals

@admin.register(Hospitals)
class MapAdmin(OSMGeoAdmin):
    list_display = ('yadmNm', 'location','telno')