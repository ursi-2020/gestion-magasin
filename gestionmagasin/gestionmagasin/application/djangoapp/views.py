from django.http import HttpResponse
from apipkg import api_manager as api


def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("L'heure de la clock est %r" % time)

def info(request):
    info = api.send_request('caisse', 'helloWorld')
    return HttpResponse("Hello je suis Gestion Magasin %r" % info)
