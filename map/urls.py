from django.urls import path, include
from . import views

urlpatterns = [
    path('maskstore/',views.maskmap),
    path('reliefhospitals/',views.hospmap),
]