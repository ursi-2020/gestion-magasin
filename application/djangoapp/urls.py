from django.urls import path

from . import views

urlpatterns = [
    # API
    path('api/products/', views.get_products, name='Get Products'),
    path('api/customers/', views.get_customers, name='Get Customers'),
    path('api/sales/', views.api_sales, name='Get/Post Sales'),
    path('api/stocks/', views.get_stocks, name='Get Stocks'),
    path('get_stocks/', views.get_stocks, name='Get Stocks'),
    path('api/sendOrder/', views.post_order, name='Receive Order'),
    path('api/promo/customersProducts/', views.get_promo_customers_products, name='Get Promo Client Products'),

    # HTML
    path('', views.index, name='index'),

    path('products/', views.show_products, name='Show Products'),
    path('products/update/', views.update_products, name='Update Products'),

    path('customers/', views.show_customers, name='Show Customers'),
    path('customers/update/', views.update_customers, name='Update Customers'),

    path('sales/', views.show_sales, name='Show Sales'),
    path('sales/update/', views.update_sales, name='Update Sales'),

    path('orders/', views.show_orders, name='Show Orders'),
    path('orders/command/', views.restock, name='Send Initial/Other Order'),

    path('clear_data/', views.clear_data, name='Clear Data'),

    path('promo/magasin', views.get_promo_magasin, name='Get Promo'),
    path('promo/client', views.get_promo_client, name='Get Promo Client'),


]
