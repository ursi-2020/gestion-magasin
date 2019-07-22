from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.infoA, name='infoA'),
    path('hello/', views.hello, name='hello'),
]