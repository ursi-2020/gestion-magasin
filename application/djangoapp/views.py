from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.template import loader
from . import models

def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("Heure A %r" % time)

def infoA(request):
        info = api.send_request('caisse', 'helloworld')
        template = loader.get_template('index.html')
        #return HttpResponse(template.render("Bonjour je m'appelle gestion magasin : %r" % info), request)
        return render(request, 'index.html')
       # return HttpResponse("Bonjour je m'appelle gestion magasin : %r" % info)

def hello():
    return HttpResponse("bonjour je suis gestion magasin")
