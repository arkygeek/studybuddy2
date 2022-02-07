# made by a human. this urls file is for only this app

from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('room/', views.room, name="room"),
]
