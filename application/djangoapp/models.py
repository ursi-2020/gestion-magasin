from django.db import models

# TODO: Rename to 'Product'
class Produit(models.Model):
    codeProduit = models.CharField(max_length=200)
    familleProduit = models.CharField(max_length=200)
    descriptionProduit = models.CharField(max_length=200)
    prix = models.PositiveIntegerField()
    date = models.DateTimeField(null=True)

class Customer(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    fidelityPoint = models.IntegerField(default=0)
    payment = models.IntegerField(default=0)
    account = models.CharField(max_length=10, default="")
    date = models.DateTimeField(null=True)

class GlobalInfo(models.Model):
    catalogue_is_up = models.BooleanField(default=True)
    products_last_update = models.DateTimeField(null=True)

    crm_is_up = models.BooleanField(default=True)
    customers_last_update = models.DateTimeField(null=True)