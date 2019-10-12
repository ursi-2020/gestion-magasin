from django.db import models


class Produit(models.Model):
    codeProduit = models.CharField(max_length=200, primary_key=True)
    familleProduit = models.CharField(max_length=200)
    descriptionProduit = models.CharField(max_length=200)
    quantiteMin = models.PositiveIntegerField(default=0)
    packaging = models.PositiveIntegerField(default=0)
    prix = models.PositiveIntegerField(default=0)


class Client(models.Model):
    idClient = models.TextField(blank=False, default="")
    prenom = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    ptsFidelite = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    paiement = models.IntegerField(default=0)
    compte = models.CharField(max_length=10, default="")


class ArticlesList(models.Model):
    codeProduit = models.CharField(max_length=20, primary_key=True)
    quantite = models.IntegerField()


class Ventes(models.Model):
    date = models.DateTimeField()
    prix = models.IntegerField()
    client = models.CharField(max_length=20)
    articles = models.ManyToManyField(ArticlesList)
    pointsFidelite = models.IntegerField()
    modePaiement = models.CharField(max_length=10)


class GlobalInfo(models.Model):
    catalogue_is_up = models.BooleanField(default=True)
    products_last_update = models.DateTimeField(null=True)

    crm_is_up = models.BooleanField(default=True)
    customers_last_update = models.DateTimeField(null=True)


class Commande(models.Model):
    codeProduit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()

class Inventaire(models.Model):
    codeProduit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
