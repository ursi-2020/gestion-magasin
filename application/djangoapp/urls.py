from django.urls import path

from . import views

# views.schedule_task_simple('/products/update/', 'day')
# views.schedule_task_simple('/customers/update/', 'day')

urlpatterns = [
    path('', views.index, name='index'),

    path('products/', views.get_products, name='Get Products'),
    path('products/update/', views.update_products, name='Update Products'),

    path('customers/', views.get_customers, name='Get Customers'),
    path('customers/update/', views.update_customers, name='Update Customers'),

]


