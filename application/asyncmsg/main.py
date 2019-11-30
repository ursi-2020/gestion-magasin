import sys
import os
import django
from apipkg import queue_manager as queue
from application.djangoapp import views


sys.dont_write_bytecode = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from application.djangoapp.models import *


def callback(ch, method, properties, body):
    print(" [x] Received from queue %r" % body)
    # jsonLoad = json.loads(body)
    # fromApp = jsonLoad["from"]
    # functionName = ""
    # if 'functionname' in jsonLoad:
    #     functionName = jsonLoad["functionname"]
    #
    # if fromApp == 'gestion-commerciale':
    #     if functionName == "magasin_get_order_response":
    #         print("received response from gesco. Body is", body)


if __name__ == '__main__':
    queue.receive('gestion-magasin', callback)
