from django.urls import path, include
from . import views

urlpatterns = [
    path('sido/', views.sidoview),
    path('apps/', views.appinfo)
]