import json

from apipkg import api_manager as api
from application.djangoapp.models import Customer

def update_customers():
    customers = api.send_request('crm', 'api/data')
    # TODO: Try to catch bad response form the send_request, when CRM is down

    Customer.objects.all().delete()

    data = json.loads(customers)
    for customer in data:
        c = Customer(firstName=customer['firstName'],
                     lastName=customer['lastName'],
                     fidelityPoint=customer['fidelityPoint'],
                     payment=customer['payment'],
                     account=customer['account'])
        c.save()