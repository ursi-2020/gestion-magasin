from datetime import datetime, timedelta

import json
import requests
from apipkg import api_manager as api
from django.forms.models import model_to_dict
from django.http import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.forms.models import model_to_dict

from .models import *


# TODO: very good documentation
# TODO: html page for 404

# TODO: See if it is possible to deserialize received data directly into objects without specifying attributes

# VIEWS FUNCTIONS

@require_GET
def index(request):
    return show_products(request)


@csrf_exempt
@require_POST
def clear_data(request):
    Client.objects.all().delete()
    Produit.objects.all().delete()
    Vente.objects.all().delete()

    GlobalInfo.objects.filter().update(
        products_last_update=None,
        customers_last_update=None,
        tickets_last_update=None
    )

    return HttpResponseRedirect('/')


# PRODUCTS

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

        for product in data['produits']:
            Produit.objects.update_or_create(
                codeProduit=product['codeProduit'],
                defaults={
                    'familleProduit': product['familleProduit'],
                    'descriptionProduit': product['descriptionProduit'],
                    'quantiteMin': product['quantiteMin'],
                    'packaging': product['packaging'],
                    'prix': product['prix']
                }
            )
        GlobalInfo.objects.update(products_last_update=get_current_datetime(), catalogue_is_up=True)
    except json.JSONDecodeError:
        GlobalInfo.objects.update(catalogue_is_up=False)

    return HttpResponseRedirect('/')


@require_GET
def show_products(request):
    products = Produit.objects.all().values()
    for product in products:
        product.update(prix=product['prix'] / 100)
    return render(request, 'products.html', create_context(products))


# END PRODUCTS

# CUSTOMERS

@require_GET
def show_customers(request):
    customers = list(Client.objects.all().values())
    return render(request, 'customers.html', create_context(customers))


@require_GET
def get_customers(request):
    account_id = request.GET.get('account')
    name = request.GET.get('firstName')
    lastname = request.GET.get('lastName')

    if account_id or name or lastname:
        return get_customer(account_id, name, lastname)

    customers = list(Client.objects.all().values())
    return JsonResponse(customers, safe=False)


@csrf_exempt
@require_POST
def update_customers(request):
    customers = api.send_request('crm', 'api/data')
    try:
        data = json.loads(customers)

        for customer in data:
            Client.objects.update_or_create(
                idClient=customer['IdClient'],
                prenom=customer['Prenom'],
                nom=customer['Nom'],
                defaults={
                    'ptsFidelite': customer['Credit'],
                    'paiement': customer['Paiement'],
                    'compte': customer['Compte']
                }
            )
        GlobalInfo.objects.update(customers_last_update=get_current_datetime(), crm_is_up=True)
    except json.JSONDecodeError:
        GlobalInfo.objects.update(crm_is_up=False)

    return HttpResponseRedirect('/customers')


# END CUSTOMERS

# SALES

@require_GET
def show_sales(request):
    ventes = Vente.objects.all().values()
    for v in ventes:
        v.update(prix=v['prix'] / 100)
    return render(request, 'sales.html', create_context(ventes))


@require_GET
def get_sales(request):
    ventes_set = Vente.objects.all()
    ventes = []

    for vente_obj in ventes_set:
        vente = model_to_dict(vente_obj)
        vente['articles'] = []
        for article_obj in vente_obj.articles.all():
            vente['articles'].append(model_to_dict(article_obj))
        ventes.append(vente)

    return JsonResponse(ventes, safe=False)


@csrf_exempt
@require_POST
def update_sales(request):
    sales = api.send_request('caisse', 'api/tickets')
    try:
        data = json.loads(sales)

        ArticleVendu.objects.all().delete()
        Vente.objects.all().delete()

        for sale in data:
            vente = Vente(date=sale['date'],
                          prix=sale['prix'],
                          client=sale['client'],
                          pointsFidelite=sale['pointsFidelite'],
                          modePaiement=sale['modePaiement'])
            vente.save()
            for article_dict in sale['articles']:
                tmp = Produit.objects.get(codeProduit=article_dict['codeProduit'])
                article = ArticleVendu(article=tmp,
                                       vente=vente,
                                       quantite=article_dict['quantity'])
                article.save()
        GlobalInfo.objects.update(tickets_last_update=get_current_datetime(), caisse_is_up=True)
    except json.JSONDecodeError:
        GlobalInfo.objects.update(caisse_is_up=False)
    return HttpResponseRedirect('/sales')


# END SALES

# def get_reapro(request):
#     ventes = Vente.objects.filter(date=get_current_datetime())
#     for article in ventes['articles']:
#         article_new = Produit.objects.get(codeProduit=article.codeProduit)
#         quantite = ventes['articles'].count(codeProduit=article_new.codeProduit)
#         quantite *= 2
#         article_commande = ArticleCommande(article=article_new,
#                                            quantite=quantite)
#         article_commande.save()
#
#     # produits = Produit.objects.filter(codeProduit=ventes.codeProduit)
#     #
#     # ArticleVendu.objects.all().update(quantite=F('quantite') * 2)
#     # produitsVendus = ArticleVendu.objects.all().values()
#     # ArticleVendu.objects.all().update(quantite=F('quantite') / 2)
#     # commande = []
#     # #for c in produitsVendus:
#
#
#
#     headers = {'Host': 'gestion-commerciale'}
#     r = requests.post(api.api_services_url + 'place-order', headers=headers, json=produitsVendus)
#     return JsonResponse(produitsVendus, safe=False)

# END VIEWS FUNCTIONS
#############################
# UTILS FUNCTIONS

# TODO: a tester
def get_customer(user_id, name, lastname):
    try:
        customer = (Client.objects.get(account=user_id) |
                    Client.objects.get(firstName=name) &
                    Client.objects.get(lastname=lastname))
    except Client.DoesNotExist:
        return HttpResponseNotFound({"Customer '" + user_id + "' does not exist."})
    customer = model_to_dict(customer)
    return JsonResponse(customer, safe=False)


def create_context(value):
    context = {
        'context': value,
        'time': get_current_datetime().strftime("%Y-%m-%d %H:%M:%S"),
        'global_info': GlobalInfo.objects.first()
    }
    return context


def get_current_datetime():
    clock_time = api.send_request('scheduler', 'clock/time').strip('"')
    return datetime.strptime(clock_time, '%d/%m/%Y-%H:%M:%S')


def get_daily_format(date):
    return datetime.strptime(date, '%d/%m/%Y')


def schedule_task_simple(name, task, recurrence):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(minutes=5)
    api.schedule_task('gestion-magasin', task, time, recurrence, '{}', 'gestion-magasin', name)

# END UTILS FUNCTIONS
