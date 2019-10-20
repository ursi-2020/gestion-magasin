from django.urls import path

from . import views

urlpatterns = [
    # TODO: differenciate api endpoints from html endpoints
    # TODO: specify methods for each endpoint

    # API
    path('api/sales', views.get_sales_data, name='Get Sales Data'),

    # HTML
    path('', views.index, name='index'),

    path('products/', views.get_products, name='Get Products'),
    path('products/update/', views.update_products, name='Update Products'),

    path('customers/', views.get_customers, name='Get Customers'),
    path('customers/update/', views.update_customers, name='Update Customers'),

    path('sales/', views.get_tickets, name='Get Sales'),
    path('sales/update/', views.update_tickets, name='Update Sales'),

    path('clear_data/', views.clear_data, name='Clear Data'),
]
