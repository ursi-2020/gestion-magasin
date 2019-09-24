import json

from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render

from application.djangoapp.models import Info
from application.djangoapp.models import Product


def index(request):
    time = api.send_request('scheduler', 'clock/time')
    if Info.objects.all():
        click = Info.objects.first()
        click.delete()
    return HttpResponse("Bienvenue sur l'application Gestion Magasin, il est: %r" % time)


def infoA(request):
    context = {
        'info': 'Pas d\'info reçu de l\'app Caisse'
    }
    if not Info.objects.all():
        click = Info(nbRequests=0)
        click.save()
    else:
        click = Info.objects.first()
        click.nbRequests = click.nbRequests + 1
        click.save()
        info = api.send_request('caisse', 'helloworld')
        context['info'] = info
    context['click'] = click
    return render(request, 'index.html', context)


def hello(request):
    return HttpResponse("Bonjour je suis gestion magasin")


def getProducts(request):
    items = api.send_request('catalogue-produit', 'catalogueproduit/api/data')
    data = json.loads(items)
    context = {
        'products': data['produits']
    }
    print(data['produits'])
    for produit in data['produits']:
        p = Product(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                    descriptionProduit=produit['descriptionProduit'], prix=produit['prix'])
        p.save()
    return render(request, 'app.html', context)
