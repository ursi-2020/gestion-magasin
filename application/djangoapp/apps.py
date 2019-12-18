import os

from django.apps import AppConfig
from apipkg import api_manager as api
from django.views.decorators.csrf import csrf_exempt

myappurl = "http://localhost:" + os.environ["WEBSERVER_PORT"]


class ApplicationConfig(AppConfig):
    name = 'application.djangoapp'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            api.unregister(os.environ['DJANGO_APP_NAME'])
            api.register(myappurl, os.environ['DJANGO_APP_NAME'])

            from .models import GlobalInfo
            global_info = GlobalInfo.objects.first()
            if not global_info:
                GlobalInfo().save()

            if 'ENV' in os.environ:
                if os.environ['ENV'] == 'dev':
                    api.post_request(host='scheduler', url='/app/delete?source=gestion-magasin', body={})

            from .views import schedule_task_simple
            schedule_task_simple('Magasin: Update Products', '/products/update/', 'day')
            schedule_task_simple('Magasin: Update Customers', '/customers/update/', 'day')
            schedule_task_simple('Magasin: Restock', '/orders/command/', 'day')
            schedule_task_simple('Magasin: Update promos Client Products', 'promo/customersProducts', 'day')
