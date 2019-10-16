import requests, json

from django.http import *
from apipkg import api_manager as api
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .models import Produit, Client, GlobalInfo, Vente, Article


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
        'customers': Client.objects.all().values(),
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
    products = api.send_request('catalogue-produit', 'api/get-magasin')
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

        GlobalInfo.objects.update(products_last_update=get_current_datetime(), catalogue_is_up=True)
    except json.JSONDecodeError:
        GlobalInfo.objects.update(catalogue_is_up=False)

    return HttpResponseRedirect('/')


# For CAISSE
@require_GET
def get_customers(request):
    account_id = request.GET.get('account')
    name = request.GET.get('firstName')
    lastname = request.GET.get('lastName')
    global_info = GlobalInfo.objects.first()
    if account_id:
        return get_customer(account_id)
    elif name:
        return get_customer(name)
    elif lastname:
        return get_customer(lastname)
    else:
        customers = list(Client.objects.all().values())
    context = {
        'customers': customers,
        'crm_is_up': global_info.crm_is_up,
        'customers_update_time': global_info.customers_last_update,
    }
    return render(request, 'clients.html', context)


@csrf_exempt
@require_POST
def update_customers(request):
    customers = api.send_request('crm', 'api/data')
    global_info = GlobalInfo.objects.first()
    try:
        data = json.loads(customers)

        Client.objects.all().delete()

        for customer in data:
            c = Client(idClient=customer['IdClient'],
                       prenom=customer['Prenom'],
                       nom=customer['Nom'],
                       ptsFidelite=customer['Credit'],
                       paiement=customer['Paiement'],
                       compte=customer['Compte'])
            c.save()

        GlobalInfo.objects.update(customers_last_update=get_current_datetime(), crm_is_up=True)
    except json.JSONDecodeError:
        GlobalInfo.objects.update(crm_is_up=False)
    cus = Client.objects.all().values()
    context = {
        'customers': cus,
        'crm_is_up': global_info.crm_is_up,
        'customers_update_time': global_info.customers_last_update,
    }
    return render(request, 'clients.html', context)


# For CAISSE
@require_GET
def get_tickets(request):
    ventes = Vente.objects.all().values()
    for v in ventes:
        v.update(prix=v['prix'] / 100)
    global_info = GlobalInfo.objects.first()
    context = {
        'ventes': ventes,
        'crm_is_up': global_info.crm_is_up,
        'customers_update_time': global_info.customers_last_update,
    }
    return render(request, 'ventes.html', context)


@csrf_exempt
@require_POST
def update_tickets(request):
    # return render(request, 'index.html')
    tickets = api.send_request('caisse', 'api/tickets')
    global_info = GlobalInfo.objects.first()
    try:
        data = json.loads(tickets)
        # print(data)
        Vente.objects.all().delete()
        for t in data:
            ticket = Vente(date=t['date'],
                            prix=t['prix'],
                            client=t['client'],
                            pointsFidelite=t['pointsFidelite'],
                            modePaiement=t['modePaiement'])
                            # articles=t['articles'])
            ticket.save()
            articles=[]
            for article_dict in t['articles']:
                article = Article(codeProduit=article_dict['codeProduit'], quantite=article_dict['quantity'])
                article.save()
                articles.append(article)
            ticket.articles.add(article)
            print(ticket.articles)
        GlobalInfo.objects.update(tickets_last_update=get_current_datetime(), caisse_is_up=True)
    except json.JSONDecodeError:
        GlobalInfo.objects.update(caisse_is_up=False)
    ventes = Vente.objects.all().values()
    context = {
        'ventes': ventes,
        'caisse_is_up': global_info.caisse_is_up,
        'tickets_update_time': global_info.tickets_last_update,
    }
    return render(request, 'ventes.html', context)


@csrf_exempt
@require_POST
def clear_all_data(request):
    Client.objects.all().delete()
    Produit.objects.all().delete()

    return HttpResponseRedirect('/')


# END VIEWS FUNCTIONS.
#####################
# UTILS FUNCTIONS:

# Todo a tester
def get_customer(user_id, name, lastname):
    try:
        customer = (Client.objects.get(account=user_id) |
                    Client.objects.get(firstName=name) &
                    Client.objects.get(lastname=lastname))
    except Client.DoesNotExist:
        return HttpResponseNotFound({"Customer '" + user_id + "' does not exist."})
    customer = model_to_dict(customer)
    return JsonResponse(customer, safe=False)


def get_current_datetime():
    clock_time = api.send_request('scheduler', 'clock/time').strip('"')
    return datetime.strptime(clock_time, '%d/%m/%Y-%H:%M:%S')


def get_daily_format(date):
    return datetime.strptime(date, '%d/%m/%Y')


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
