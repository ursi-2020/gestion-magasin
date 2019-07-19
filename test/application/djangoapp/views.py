from django.http import HttpResponse
from apipkg import api_manager as api


def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("Heure B %r" % time)

def infoB(request):
        #time = api.send_request('InfoA', 'infoA')
        return HttpResponse("Hello it's me B")

