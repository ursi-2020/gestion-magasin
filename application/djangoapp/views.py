from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render

from application.djangoapp.models import Info

def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("Heure A %r" % time)

def infoA(request):
    if not Info.objects.all():
        click = Info(nbRequests=0)
        click.save()
    else:
        info = api.send_request('caisse', 'helloworld')
        click = Info.objects.first()
        click.nbRequests = click.nbRequests + 1
        click.save()
        context = {
            'info': info,
            'click': click,
        }
    return render(request, 'index.html', context)

def hello(request):
    return HttpResponse("Bonjour je suis gestion magasin")
