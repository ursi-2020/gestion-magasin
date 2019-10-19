from django.urls import path

from . import views

urlpatterns = [
    # TODO: differenciate api endpoints from html endpoints
    # TODO: specify methods for each endpoint

    path('api/sales', views.get_sales_data, name='Get Sales Data'),

    #For CAISSE
    path('products/', views.get_products, name='Get Products'),
    path('products/update/', views.update_products, name='Update Products'),

    #For CAISSE
    path('customers/', views.get_customers, name='Get Customers'),
    path('customers/update/', views.update_customers, name='Update Customers'),

    #For my APP
    path('daily_tickets/', views.get_tickets, name='Get daily tickets'),
    path('daily_tickets/update/', views.update_tickets, name='Update tickets'),
    path('clear_all_data/', views.clear_all_data, name='Clear All Data'),

    path('', views.index, name='index'),
]
