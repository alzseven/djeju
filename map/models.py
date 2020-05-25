from django.conf import settings
from django.db import models
from django.utils import timezone


class MaskStores(models.Model):
    addr = models.CharField(max_length = 200)
    code = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length = 200)
