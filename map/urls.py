from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.map, name='map'),
    path('maskstore/',views.maskmap),
    #path('<str:lat>/<str:lng>',views.curmap, name='loc'),
    #path('')
]