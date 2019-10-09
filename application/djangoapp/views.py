import requests, json

from django.http import *
from apipkg import api_manager as api
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .models import Produit, Customer, GlobalInfo


# TODO: very good documentation
# TODO: html page for 404

# TODO: Save all received data in one shot, to avoid partial rendering of data in middle of processing
# TODO: See if it is possible to deserialize received data directly into objects without specifying attributes

# VIEWS FUNCTIONS:

# Only shows the current data of the database, does not update it from remote apps
@require_GET
def index(request):
    products = Produit.objects.all().values()
    for product in products:
        product.update(prix=product['prix'] / 100)

    global_info = GlobalInfo.objects.first()

    context = {
        'time': get_current_datetime().strftime("%Y-%m-%d %H:%M:%S"),
        'products': products,
        'customers': Customer.objects.all().values(),
        'products_update_time': global_info.products_last_update,
        'catalogue_is_up': global_info.catalogue_is_up,
        'customers_update_time': global_info.customers_last_update,
        'crm_is_up': global_info.crm_is_up,
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

    try:
        data = json.loads(products)
        Produit.objects.all().delete()

        for product in data['produits']:
            p = Produit(codeProduit=product['codeProduit'],
                        familleProduit=product['familleProduit'],
                        descriptionProduit=product['descriptionProduit'],
                        quantiteMin=product['quantiteMin'],
                        packaging=product['packaging'],
                        prix=product['prix'])
            p.save()

        GlobalInfo.objects.update(products_last_update = get_current_datetime(), catalogue_is_up=True)
    except json.JSONDecodeError:
        GlobalInfo.objects.update(catalogue_is_up = False)

    return HttpResponseRedirect('/')


# For CAISSE
@require_GET
def get_customers(request):
    account_id = request.GET.get('account')
    name = request.GET.get('firstName')
    lastname = request.GET.get('lastName')
    if account_id:
        return get_customer(account_id)
    elif name:
        return get_customer(name)
    elif lastname:
        return get_customer(lastname)
    else:
        customers = list(Customer.objects.all().values())
    return JsonResponse(customers, safe=False)


@csrf_exempt
@require_POST
def update_customers(request):
    customers = api.send_request('crm', 'api/data')

    try:
        data = json.loads(customers)

        Customer.objects.all().delete()

        for customer in data:
            c = Customer(idClient=customer['id'],
                         firstName=customer['Nom'],
                         lastName=customer['Prenom'],
                         fidelityPoint=customer['Credit'],
                         payment=customer['Paiement'],
                         account=customer['Compte'])
            c.save()

        GlobalInfo.objects.update(customers_last_update = get_current_datetime(), crm_is_up = True)
    except json.JSONDecodeError:
        GlobalInfo.objects.update(crm_is_up = False)

    return HttpResponseRedirect('/')

@csrf_exempt
@require_POST
def clear_all_data(request):
    Customer.objects.all().delete()
    Produit.objects.all().delete()

    return HttpResponseRedirect('/')


#def getClientProducts()
# END VIEWS FUNCTIONS.
#####################
# UTILS FUNCTIONS:

def get_customer(user_id, name, lastname):
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


def schedule_task_simple(name, task, recurrence):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(minutes=5)
    schedule_task('gestion-magasin', task, time, recurrence, '{}', 'gestion-magasin', name)

# END UTILS FUNCTIONS.
