from datetime import datetime, timedelta

import json
import os
import requests
from apipkg import api_manager as api
from apipkg import queue_manager as queue
from django.forms.models import model_to_dict
from django.http import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.forms.models import model_to_dict
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from apipkg import queue_manager as queue
from .models import *
import os


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
    CustomersProducts.objects.all().delete()

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
    if products == '{"message":"no Route matched with those values"}':
        GlobalInfo.objects.update(catalogue_is_up=False)
    else:
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
                        'prix': product['prix'],
                    }
                )
            GlobalInfo.objects.update(products_last_update=get_current_datetime(), catalogue_is_up=True)
            get_promo_magasin(request)
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
    promos = list(CustomersProducts.objects.all().values())
    return render(request, 'customers.html', create_context({
        'customers': customers,
        'promos': promos
    }))


@require_GET
def get_customers(request):
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
    if customers == '{"message":"no Route matched with those values"}':
        GlobalInfo.objects.update(crm_is_up=False)
    else:
        try:
            data = json.loads(customers)
            for customer in data:
                Client.objects.update_or_create(
                    idClient=customer['IdClient'],
                    prenom=customer['Prenom'],
                    nom=customer['Nom'],
                    defaults={
                        'ptsFidelite': customer['Credit'],
                        'compte': customer['Compte'],
                    }
                )
                CustomersProducts.objects.update_or_create(
                    idClient=customer['IdClient']
                )
            GlobalInfo.objects.update(customers_last_update=get_current_datetime(), crm_is_up=True)
            get_promo_client(request)
            # get_promo_customers_products(request)
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
            article_vendu_obj = ArticleVendu.objects.filter(article=article_obj, vente=vente_obj)[0]
            vente_dict = model_to_dict(article_obj)
            vente_dict['quantity'] = article_vendu_obj.quantity
            vente['articles'].append(vente_dict)
            if vente['client']:
                try:
                    vente['CustomerPromo'] = CustomersProducts.objects.filter(idClient=vente['client'],
                                                                      codeProduit=article_obj.codeProduit)[0].promo
                except Exception as e :
                    print(e)
                    vente['CustomerPromo'] = 0
        if vente['client']:
            try:
                vente['GlobalPromo'] = Client.objects.filter(idClient=vente['client'])[0].promo
            except Exception as e:
                print(e)
                vente['GlobalPromo'] = 0
        ventes.append(vente)

    return JsonResponse({'tickets': ventes}, safe=False)


@require_POST
def post_sales(request):
    sale = json.loads(request.POST.get("ticket"))

    vente = Vente.objects.create(
        date=datetime.strptime(sale['date'], '%d/%m/%Y-%H:%M:%S'),
        prix=sale['prix'],
        client=sale['client'],
        pointsFidelite=sale['pointsFidelites'],
        modePaiement=sale['modePaiement']
    )
    for article in json.loads(sale['articles']):
        tmp = Produit.objects.get(codeProduit=article['codeProduit'])
        ArticleVendu.objects.create(
            article=tmp,
            vente=vente,
            quantity=article['quantity']
        )

    GlobalInfo.objects.update(tickets_last_update=get_current_datetime(), caisse_is_up=True)

    return HttpResponse('Sale received.')


@csrf_exempt
@require_POST
def update_sales(request):
    sales = api.send_request('caisse', 'api/tickets')
    if sales == '{"message":"no Route matched with those values"}':
        GlobalInfo.objects.update(caisse_is_up=False)
    else:
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
                        quantity=article_dict['quantity']
                    )
            GlobalInfo.objects.update(tickets_last_update=get_current_datetime(), caisse_is_up=True)
            update_stock()
        except json.JSONDecodeError:
            GlobalInfo.objects.update(caisse_is_up=False)

    return HttpResponseRedirect('/sales')


# endregion

# region GesCo orders related functions

@require_GET
def show_orders(request):
    orders = Commande.objects.all()
    return render(request, 'orders.html', create_context(orders))


@require_GET
def get_reapro(request):
    commande = list(ArticleCommande.objects.all().values())
    return JsonResponse(commande, safe=False)



# Recieve order from GesCo
def post_order(cmd):
    order = json.loads(cmd)
    order = order['body']
    try:

        for produit in order['produits']:
            tmp = Produit.objects.get(codeProduit=produit['codeProduit'])
            tmp.stock += produit['quantite']
            tmp.save()

        commande = Commande.objects.get(id=order['idCommande'])
        commande.statut = "Reçue"
        commande.save()
    except:
        print('Tried to deliver: ', order['idCommande'], ' but didn\'t work, maybe it doesn\'t exist')

    return HttpResponse('Order received')


@csrf_exempt
@require_POST
def request_restock(request):
    articles_vendus = ArticleVendu.objects.all()
    article_commandes = {}

    for article_vendu in articles_vendus:
        if str(article_vendu.article_id) in article_commandes:
            article_commandes[str(article_vendu.article_id)] += article_vendu.quantity
        else:
            article_commandes[str(article_vendu.article_id)] = article_vendu.quantity

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
        'produits': produits_body
    }

    headers = {'Host': 'gestion-commerciale'}

    send_async_msg('gestion-commerciale', request_body, 'get_order_magasin')

    return HttpResponseRedirect('/orders')


@csrf_exempt
@require_POST
def request_restock_init(request):
    GlobalInfo.objects.update(is_first_reapro=False)
    articles = Produit.objects.all()
    article_commandes = {}

    for a in articles:
        article_commandes[str(a.codeProduit)] = a.stock

    commande = Commande.objects.create(date=get_current_datetime())

    produits_body = []

    for code_produit, quantite in article_commandes.items():
        ArticleCommande.objects.create(
            article=Produit.objects.get(codeProduit=code_produit),
            commande=commande,
            quantite=25
        )
        produits_body.append({
            'codeProduit': code_produit,
            'quantite': 25
        })

    request_body = {
        'idCommande': commande.id,
        'produits': produits_body
    }
    # if produits_body != []:
    send_async_msg('gestion-commerciale', request_body, 'get_order_magasin')

    return HttpResponseRedirect('/orders')


@csrf_exempt
@require_POST
def restock(request):
    if ArticleCommande.objects.exists():
        return request_restock(request)
    return request_restock_init(request)


# endregion

# region Stock related functions

@require_GET
def get_stocks(request):
    return JsonResponse(send_stock(), safe=False)

def send_stock():
    articles = Produit.objects.all()
    result = []
    for article in articles:
        a = dict()
        a['numeroFournisseur'] = 1
        a['stockDisponible'] = article.stock
        a['codeProduit'] = a['codeFournisseur'] = article.codeProduit
        result.append(a)
    send_async_msg('business-intelligence', str({"stock": result}), "get_stock_magasin")
    result = {'stocks': result}
    return result

def update_stock():
    articlesVendus = ArticleVendu.objects.all()
    for a in articlesVendus:
        produit = Produit.objects.get(codeProduit=a.article_id)
        if produit.stock > 0:
            produit.stock -= a.quantity
        produit.save()


# end region

# region Promo related functions

def get_promo_magasin(request):
    data = api.send_request('gestion-promotion', 'promo/magasin')
    print(data)
    try:
        promos = json.loads(data)
        # clear_promos_produits()
        for promo in promos['promo']:
            p = Produit.objects.get(codeProduit=promo['codeProduit'])
            p.promo = promo['reduction']
            p.prixApres = promo['prix'] / 100
            p.save()
    except:
        print("Couldn't load json")


def get_promo_client(request):
    data = api.send_request('gestion-promotion', 'promo/customers')
    try:
        promos = json.loads(data)
        # clear_promos_customers()
        for promo in promos['promo']:
            p = Client.objects.get(idClient=promo['IdClient'])
            p.promo = promo['reduction']
            p.save()
    except:
        print("Couldn't load json")

@csrf_exempt
@require_POST
def update_promo_customers_products(request):
    data = api.send_request('gestion-promotion', 'promo/customersproducts')
    try:
        promos = json.loads(data)
        CustomersProducts.objects.all().delete()
        for p in promos['promo']:
            CustomersProducts.objects.update_or_create(
                idClient=p['IdClient'],
                codeProduit=p['codeProduit'],
                promo=p['reduction']
            )
    except:
        print("Couldn't load json")

    return HttpResponseRedirect('/customers')

@require_GET
def get_promo_customers_products(request):
    idClient = request.GET.get('idClient')
    codeProduit = request.GET.get('codeProduit')
    try:
        data = CustomersProducts.objects.filter(idClient=idClient, codeProduit=codeProduit)[0]
        promo = data.promo
    except Exception as e:
        promo = 0
    return JsonResponse({'promo': promo})

def clear_promos_produits(request):
    produits = Produit.objects.all()
    for p in produits:
        p.promo = 0
        p.prixApres = p.prix
        p.save()

def clear_promos_customers(request):
    customers = Client.objects.all()
    for c in customers:
        c.promo = 0
        c.save()

# end region

# region UTILS FUNCTIONS


def get_customer(IdClient, prenom, nom):
    try:
        customer = Client.objects.filter(Q(idClient=IdClient) | Q(prenom=prenom) | Q(nom=nom))
    except Client.DoesNotExist:
        return HttpResponseNotFound({"Customer '" + IdClient + "' does not exist."})
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


def send_async_msg(to, body, function_name):
    time = api.send_request('scheduler', 'clock/time')
    message = '{ "from":"' + os.environ[
        'DJANGO_APP_NAME'] + '", "to": "' + to + '", "datetime": ' + time + ', "body": ' + json.dumps(
        body) + ', "functionname":"' + function_name + '"}'
    queue.send(to, message)

# endregion
