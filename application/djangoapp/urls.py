from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.get_products, name='Get Products'),
    path('customers/', views.get_customers, name='Get Customers'),
    path('customers/<str:user_id>', views.get_customer, name='Get Customer'),
]