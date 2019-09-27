import requests, json

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from apipkg import api_manager as api
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from application.djangoapp.models import Produit, Customer
from datetime import datetime, timedelta


# TODO: very good documentation

# Function to schedule a task
def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data,
            "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers=headers, json=data)
    print(r.status_code)
    print(r.text)
    return r.text


def schedule_task_simple(task, recurrence):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=10)
    schedule_task('gestion-magasin', task, time, recurrence, '{}', 'gestion-magasin', task)

# Only shows the current data of the database, does not update it
def index(request):
    products = Produit.objects.all().values()
    for product in products:
        product.update(prix=product['prix'] / 100)

    products_update_time = ""
    latest = Produit.objects.latest('date')
    if latest:
        products_update_time = latest.date

    customers_update_time = ""
    latest = Customer.objects.latest('date')
    if latest:
        customers_update_time = latest.date

    context = {
        'time': get_current_datetime().strftime("%Y-%m-%d %H:%M:%S"),
        'products': products,
        'customers': Customer.objects.all().values(),
        'products_update_time': products_update_time,
        'customers_update_time': customers_update_time
    }
    return render(request, 'index.html', context)


# For CAISSE
def get_products(request):
    products = list(Produit.objects.all().values())
    return JsonResponse(products, safe=False)


@csrf_exempt
def update_products(request):
    # TODO: Check if the request type is a POST, if not, return error

    products = api.send_request('catalogue-produit', 'api/data')
    # TODO: Try to catch bad response form the send_request, when CATALOGUE is down

    Produit.objects.all().delete()

    data = json.loads(products)
    for product in data['produits']:
        p = Produit(codeProduit=product['codeProduit'],
                    familleProduit=product['familleProduit'],
                    descriptionProduit=product['descriptionProduit'],
                    prix=product['prix'],
                    date=get_current_datetime())
        p.save()

    return HttpResponseRedirect('/')


# For CAISSE
def get_customers(request):
    customers = list(Customer.objects.all().values())
    return JsonResponse(customers, safe=False)


# For CAISSE
def get_customer(request, user_id):
    try:
        customer = Customer.objects.get(account=user_id)
    except Customer.DoesNotExist:
        # TODO: Return an HTTP error instead of a JSON response
        return JsonResponse({"Error": "customer does not exist"})
    customer = model_to_dict(customer)
    return JsonResponse(customer, safe=False)

@csrf_exempt
def update_customers(request):
    # TODO: Check if the request type is a POST, if not, return error

    customers = api.send_request('crm', 'api/data')
    # TODO: Try to catch bad response form the send_request, when CRM is down

    Customer.objects.all().delete()

    data = json.loads(customers)
    for customer in data:
        c = Customer(firstName=customer['firstName'],
                     lastName=customer['lastName'],
                     fidelityPoint=customer['fidelityPoint'],
                     payment=customer['payment'],
                     account=customer['account'],
                     date=get_current_datetime())
        c.save()

    return HttpResponseRedirect('/')


def get_current_datetime():
    clock_time = api.send_request('scheduler', 'clock/time').strip('"')
    return datetime.strptime(clock_time, '%d/%m/%Y-%H:%M:%S')
