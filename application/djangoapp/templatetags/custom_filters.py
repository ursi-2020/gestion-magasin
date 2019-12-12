from django import template
from ..models import *

register = template.Library()


@register.filter(name='quantity')
def quantity(vente, article):
    result = 0
    articlesVendus = ArticleVendu.objects.filter(article=article, vente=vente)
    for articleVendu in articlesVendus:
        result += articleVendu.quantite
    return result


@register.filter(name='quantity_ordered')
def quantity(commande, article):
    result = 0
    articlesCommande = ArticleCommande.objects.filter(article=article, commande=commande)
    for articleCommande in articlesCommande:
        result += articleCommande.quantite
    return result
