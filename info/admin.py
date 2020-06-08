from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Sido
# Register your models here.

@admin.register(Sido)
class SidoAdmin(OSMGeoAdmin):
    list_display = ('gubun', 'inc_dec','create_dt')