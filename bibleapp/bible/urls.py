from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bible-home'),
    path('display', views.display, name='display'),
    path('nextpage', views.nextpage, name='nextpage'),
    path('prevpage', views.prevpage, name='prevpage'),
    path('split', views.split, name='split'),
    path('VoiceControl', views.VoiceControl, name='VoiceControl'),
    
]