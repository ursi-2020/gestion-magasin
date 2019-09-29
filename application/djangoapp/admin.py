from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Produit)
admin.site.register(models.Customer)
admin.site.register(models.GlobalInfo)