from django.http import HttpResponse
from apipkg import api_manager as api


def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("Heure A %r" % time)

def infoA(request):
        infoB = api.send_request('caisse', 'helloworld')
        return HttpResponse("Bonjour je m'appelle gestion magasin : %r" % infoB)
        #return HttpResponse("Hello i'm GM")

def hello():
    return HttpResponse("bonjour je suis gestion magasin")
