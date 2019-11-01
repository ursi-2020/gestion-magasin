from datetime import datetime, timedelta

import json
import requests
from apipkg import api_manager as api
from django.forms.models import model_to_dict
from django.http import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.forms.models import model_to_dict
from django.db.models import Q

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

    ArticleVendu.objects.all().delete()
    ArticleCommande.objects.all().delete()
    Commande.objects.all().delete()
    Produit.objects.all().delete()
    Vente.objects.all().delete()

    GlobalInfo.objects.filter().update(
        products_last_update=None,
        customers_last_update=None,
        tickets_last_update=None
    )

    return HttpResponseRedirect('/')


# region Products related functions
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
    products = Produit.objects.all()
    for product in products:
        product.prix = product.prix / 100
    return render(request, 'products.html', create_context(products))


# endregion

# region Customers related functions

@require_GET
def show_customers(request):
    customers = list(Client.objects.all().values())
    return render(request, 'customers.html', create_context(customers))


@require_GET
def get_customers(request):
    # Changer nom en français
    carteFid = request.GET.get('carteFid')
    prenom = request.GET.get('prenom')
    nom = request.GET.get('nom')

    if carteFid or prenom or nom:
        return get_customer(carteFid, prenom, nom)

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
                    'compte': customer['Compte'],
                    'carteFid': customer['carteFid']
                }
            )
        GlobalInfo.objects.update(customers_last_update=get_current_datetime(), crm_is_up=True)
    except json.JSONDecodeError:
        GlobalInfo.objects.update(crm_is_up=False)

    return HttpResponseRedirect('/customers')


# endregion

# region Sales related functions

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def api_sales(request):
    if request.method == 'GET':
        return get_sales(request)
    return post_sales(request)


@require_GET
def show_sales(request):
    ventes = Vente.objects.all()
    for vente in ventes:
        vente.prix = vente.prix / 100
    return render(request, 'sales.html', create_context({
        'ventes': ventes,
        'articles_vendus': ArticleVendu.objects.all()
    }))


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


@require_POST
def post_sales(request):
    print('Receiving sales')
    return HttpResponse('Thanks')


@csrf_exempt
@require_POST
def update_sales(request):
    sales = api.send_request('caisse', 'api/tickets')
    try:
        data = json.loads(sales)

        ArticleVendu.objects.all().delete()
        Vente.objects.all().delete()

        for sale in data:
            vente = Vente.objects.create(
                date=sale['date'],
                prix=sale['prix'],
                client=sale['client'],
                pointsFidelite=sale['pointsFidelite'],
                modePaiement=sale['modePaiement']
            )
            for article_dict in sale['articles']:
                tmp = Produit.objects.get(codeProduit=article_dict['codeProduit'])
                ArticleVendu.objects.create(
                    article=tmp,
                    vente=vente,
                    quantite=article_dict['quantity']
                )
        GlobalInfo.objects.update(tickets_last_update=get_current_datetime(), caisse_is_up=True)
    except json.JSONDecodeError:
        GlobalInfo.objects.update(caisse_is_up=False)
    return HttpResponseRedirect('/sales')


# endregion

# region GesCo orders related functions

# Todo : changer les noms de variables

@require_GET
def show_orders(request):
    orders = Commande.objects.all()
    return render(request, 'orders.html', create_context(orders))


@csrf_exempt
@require_POST
def request_restock(request):
    articles_vendus = ArticleVendu.objects.all()
    article_commandes = {}

    for article_vendu in articles_vendus:
        if str(article_vendu.article_id) in article_commandes:
            article_commandes[str(article_vendu.article_id)] += article_vendu.quantite
        else:
            article_commandes[str(article_vendu.article_id)] = article_vendu.quantite

    commande = Commande.objects.create(date=get_current_datetime())

    produits_body = []

    for code_produit, quantite in article_commandes.items():
        ArticleCommande.objects.create(
            article=Produit.objects.get(codeProduit=code_produit),
            commande=commande,
            quantite=(quantite * 2)
        )
        produits_body.append({
            'codeProduit': code_produit,
            'quantite': (quantite * 2)
        })

    request_body = {
        'idCommande': commande.id,
        'Produits': produits_body
    }

    headers = {'Host': 'gestion-commerciale'}

    # TODO: use api-manager function for post request instead
    r = requests.post(api.api_services_url + 'place-order', headers=headers, data=json.dumps(request_body))

    return HttpResponseRedirect('/orders')


@require_GET
def get_reapro(request):
    commande = list(ArticleCommande.objects.all().values())
    return JsonResponse(commande, safe=False)


@require_POST
def receive_order(request):
    print("Receiving order")
    return HttpResponse('Thanks')


# endregion

# region Stock related functions

@require_GET
def get_stocks(request):
    stocks = {
        'X1-0': 0,
        'X1-1': 0,
        'X1-2': 0,
        'X1-3': 0,
        'X1-8': 0,
        'X1-9': 0,
        'X1-10': 0,
    }
    return JsonResponse(stocks, safe=False)


# endregion

# region UTILS FUNCTIONS

# TODO: a tester
def get_customer(carteFid, prenom, nom):
    try:
        customer = Client.objects.filter(Q(carteFid=carteFid) | Q(prenom=prenom) | Q(nom=nom))
    except Client.DoesNotExist:
        return HttpResponseNotFound({"Customer '" + carteFid + "' does not exist."})
    customer = list(customer.values())
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

# endregion
