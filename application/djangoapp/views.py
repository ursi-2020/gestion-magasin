from django.http import JsonResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.forms.models import model_to_dict

from application.djangoapp.models import Produit, Customer
from application.djangoapp.customer_utils import update_customers
from application.djangoapp.product_utils import update_products

# Only shows the current data of the database, does not update it
def index(request):
    update_products() # TODO: remove this and schedule the update
    update_customers() # TODO: remove this and schedule the update
    context = {
        'time': api.send_request('scheduler', 'clock/time'),
        'products': Produit.objects.all().values(),
        'customers': Customer.objects.all().values()
    }
    return render(request, 'app.html', context)

# For CAISSE
def get_products(request):
    update_products() # TODO: remove this and schedule the update
    products = list(Produit.objects.all().values())
    return JsonResponse(products, safe=False)

# For CAISSE
def get_customers(request):
    update_customers() # TODO: remove this and schedule the update
    customers = list(Customer.objects.all().values())
    return JsonResponse(customers, safe=False)

# For CAISSE
def get_customer(request, user_id):
    update_customers() # TODO: remove this and schedule the update
    try:
        customer = Customer.objects.get(account=user_id)
    except Customer.DoesNotExist:
        # TODO: Return an HTTP error instead of a JSON response
        return JsonResponse({"Error": "customer does not exist"})
    customer = model_to_dict(customer)
    return JsonResponse(customer, safe=False)
