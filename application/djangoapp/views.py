import json

from django.http import HttpResponse, JsonResponse
from apipkg import api_manager as api
from django.shortcuts import render

from application.djangoapp.models import Info
from application.djangoapp.models import Produit
from application.djangoapp.models import Customer


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
    # Try to catch bad response form the send_request, when catalogue porduit is down
    data = json.loads(items)
    Produit.objects.all().delete()
    for produit in data['produits']:
        p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                    descriptionProduit=produit['descriptionProduit'], prix=produit['prix'])
        p.save()
    context = {
        'products': Produit.objects.all().values()
    }

    return render(request, 'app.html', context)


def sendProducts(request):
    products = list(Produit.objects.all().values())
    return JsonResponse({'produits': products})


def getCustomers(request):
    customers = api.send_request('crm', 'api/data')
    data = json.loads(customers)
    Customer.objects.all().delete()

    for customer in data:
        c = Customer(firstName=customer['firstName'], lastName=customer['lastName'],
                     fidelityPoint=customer['fidelityPoint'], payment=customer['payment'],
                     account=customer['account'])

        c.save()
    context = {
        'customers': Customer.objects.all().values()
    }
    return render(request, 'app.html', context)


def sendCustomers(request):
    customers = list(Customer.objects.all().values())
    return JsonResponse({'customers': customers})


def sendCustomer(request, userId):
    try:
        customer = Customer.objects.filter(id=userId).values()
    except Customer.DoesNotExist:
        return JsonResponse({"Error": "customer does not exist"})
    if customer:
        customer = list(customer)
        #print("Here: ", customer)
    return JsonResponse(customer, safe=False)
