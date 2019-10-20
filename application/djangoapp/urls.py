from django.urls import path

from . import views

urlpatterns = [
    # API
    path('api/products/', views.get_products, name='Get Products'),
    path('api/customers/', views.get_products, name='Get Customers'),
    path('api/sales/', views.get_sales, name='Get Sales'),

    # HTML
    path('', views.index, name='index'),

    path('products/', views.show_products, name='Show Products'),
    path('products/update/', views.update_products, name='Update Products'),

    path('customers/', views.show_customers, name='Show Customers'),
    path('customers/update/', views.update_customers, name='Update Customers'),

    path('sales/', views.show_sales, name='Show Sales'),
    path('sales/update/', views.update_sales, name='Update Sales'),

    path('clear_data/', views.clear_data, name='Clear Data'),
]
