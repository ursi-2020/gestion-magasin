from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.infoA, name='infoA'),
    path('hello/', views.hello, name='hello'),
    path('products/', views.getProducts, name='getProducts'),
    path('api/products/', views.sendProducts, name='sendProducts'),
    path('customers/', views.getCustomers, name='getCustomers'),
    path('api/customers/', views.sendCustomers, name='sendCustomers'),

]