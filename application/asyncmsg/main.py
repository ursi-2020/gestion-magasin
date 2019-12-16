import sys
import os
import django
import json
from apipkg import queue_manager as queue


sys.dont_write_bytecode = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from application.djangoapp.models import *
from application.djangoapp import views


def callback(ch, method, properties, body):
    print(" [x] Received from queue %r" % body)
    jsonLoad = json.loads(body)
    fromApp = jsonLoad["from"]
    functionName = ""
    if 'functionname' in jsonLoad:
        functionName = jsonLoad["functionname"]

    if fromApp == 'gestion-commerciale':
        if functionName == "get_order_response":
            views.post_order(body)
        else:
            print("Le nom de la func existe pas", functionName)
    elif fromApp == 'business-intelligence':
        if functionName == 'ask_for_stock':
            views.send_stock()
        else:
            print("Le nom de la func existe pas", functionName)
    else:
        print("requete reçue jsais pas quoi faire")


if __name__ == '__main__':
    queue.receive('gestion-magasin', callback)
