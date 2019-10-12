from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Produit)
admin.site.register(models.Client)
admin.site.register(models.GlobalInfo)