import requests, json

from django.http import *
from apipkg import api_manager as api
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from application.djangoapp.models import Produit, Customer
from datetime import datetime, timedelta
from django.views.decorators.http import require_http_methods, require_GET, require_POST


# TODO: very good documentation
# TODO: html page for 404

# VIEWS FUNCTIONS:

# Only shows the current data of the database, does not update it
@require_GET
def index(request):
    products = Produit.objects.all().values()
    for product in products:
        product.update(prix=product['prix'] / 100)

    try:
        latest = Produit.objects.latest('date')
        products_update_time = latest.date
    except Produit.DoesNotExist:
        products_update_time = ""

    try:
        latest = Customer.objects.latest('date')
        customers_update_time = latest.date
    except Customer.DoesNotExist:
        customers_update_time = ""

    context = {
        'time': get_current_datetime().strftime("%Y-%m-%d %H:%M:%S"),
        'products': products,
        'customers': Customer.objects.all().values(),
        'products_update_time': products_update_time,
        'customers_update_time': customers_update_time
    }
    return render(request, 'index.html', context)


# For CAISSE
@require_GET
def get_products(request):
    products = list(Produit.objects.all().values())
    return JsonResponse(products, safe=False)


@csrf_exempt
@require_POST
def update_products(request):
    products = api.send_request('catalogue-produit', 'api/data')

    # TODO: do not delete CATALOGUE is down
    Produit.objects.all().delete()

    # TODO: store last updated time when empty database
    # Save dummy row in case of empty response from CATALOGUE, to store last updated time
    # Produit(codeProduit='', familleProduit='', descriptionProduit='', prix=0, date=get_current_datetime()).save()

    try:
        data = json.loads(products)
        for product in data['produits']:
            p = Produit(codeProduit=product['codeProduit'],
                        familleProduit=product['familleProduit'],
                        descriptionProduit=product['descriptionProduit'],
                        prix=product['prix'],
                        date=get_current_datetime())
            p.save()
    except json.JSONDecodeError:
        pass

    return HttpResponseRedirect('/')


# For CAISSE
@require_GET
def get_customers(request):
    account_id = request.GET.get('account')
    if account_id:
        return get_customer(account_id)
    else:
        customers = list(Customer.objects.all().values())
    return JsonResponse(customers, safe=False)


@csrf_exempt
@require_POST
def update_customers(request):
    customers = api.send_request('crm', 'api/data')

    # TODO: do not delete CRM is down
    Customer.objects.all().delete()

    # TODO: store last updated time when empty database
    # Save dummy row in case of empty response from CRM, to store last updated time
    # Customer(firstName='', lastName='', fidelityPoint=0, payment=0, account='', date=get_current_datetime()).save()

    try:
        data = json.loads(customers)
        for customer in data:
            c = Customer(firstName=customer['firstName'],
                         lastName=customer['lastName'],
                         fidelityPoint=customer['fidelityPoint'],
                         payment=customer['payment'],
                         account=customer['account'],
                         date=get_current_datetime())
            c.save()
    except json.JSONDecodeError:
        pass

    return HttpResponseRedirect('/')


# END VIEWS FUNCTIONS.
#####################
# UTILS FUNCTIONS:

def get_customer(user_id):
    try:
        customer = Customer.objects.get(account=user_id)
    except Customer.DoesNotExist:
        return HttpResponseNotFound({"Customer '" + user_id + "' does not exist."})
    customer = model_to_dict(customer)
    return JsonResponse(customer, safe=False)


def get_current_datetime():
    clock_time = api.send_request('scheduler', 'clock/time').strip('"')
    return datetime.strptime(clock_time, '%d/%m/%Y-%H:%M:%S')


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

# END UTILS FUNCTIONS.
