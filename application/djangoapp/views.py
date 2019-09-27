import requests
from django.http import JsonResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.forms.models import model_to_dict

from application.djangoapp.models import Produit, Customer
from application.djangoapp.customer_utils import update_customers
from application.djangoapp.product_utils import update_products

# TODO: good documentation

# Function to schedule a task
def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data, "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    print(r.status_code)
    print(r.text)
    return r.text

# Only shows the current data of the database, does not update it
def index(request):
    update_products() # TODO: remove this and schedule the update
    update_customers() # TODO: remove this and schedule the update

    products = Produit.objects.all().values()
    for product in products:
        product.update(prix=product['prix']/100)
    context = {
        'time': api.send_request('scheduler', 'clock/time'),
        'products': products,
        'customers': Customer.objects.all().values()
    }
    return render(request, 'index.html', context)

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
