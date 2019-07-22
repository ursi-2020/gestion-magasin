from django.http import HttpResponse
from apipkg import api_manager as api


def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("Heure A %r" % time)

def infoA(request):
        infoB = api.send_request('test', 'infoBTest')
        return HttpResponse("Hello I'm Gestion Magasin and I'm talking to : %r" % infoB)
        #return HttpResponse("Hello i'm GM")

def hello():
    return HttpResponse("Hello i'm gestion magasin")
