import os

from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    name = 'application.djangoapp'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from .models import GlobalInfo
            global_info = GlobalInfo.objects.first()
            if not global_info:
                GlobalInfo().save()

            from .views import schedule_task_simple
            schedule_task_simple('Magasin: Update Products', '/products/update/', 'minute')
            schedule_task_simple('Magasin: Update Customers', '/customers/update/', 'minute')
