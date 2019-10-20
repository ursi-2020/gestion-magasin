from django import template
from ..models import *

register = template.Library()


@register.filter(name='quantity')
def quantity(vente, article):
    result = ArticleVendu.objects.get(article=article, vente=vente).quantite
    return result
