from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.get_products, name='Get Products'),
    path('products/update/', views.update_products, name='Update Products'),

    path('customers/', views.get_customers, name='Get Customers'),
    path('customers/update/', views.update_customers, name='Update Customers'),

    path('clear_all_data/', views.clear_all_data, name='Clear All Data'),

    path('', views.index, name='index'),
]
