import json

from apipkg import api_manager as api
from application.djangoapp.models import Produit

def update_products():
    items = api.send_request('catalogue-produit', 'api/data')
    # TODO: Try to catch bad response form the send_request, when CATALOGUE is down

    Produit.objects.all().delete()

    data = json.loads(items)
    for product in data['produits']:
        p = Produit(codeProduit=product['codeProduit'],
                    familleProduit=product['familleProduit'],
                    descriptionProduit=product['descriptionProduit'],
                    prix=product['prix'])
        p.save()