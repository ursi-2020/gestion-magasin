from django.db import models


class GlobalInfo(models.Model):
    catalogue_is_up = models.BooleanField(default=True)
    products_last_update = models.DateTimeField(null=True)

    crm_is_up = models.BooleanField(default=True)
    customers_last_update = models.DateTimeField(null=True)

    caisse_is_up = models.BooleanField(default=True)
    tickets_last_update = models.DateTimeField(null=True)

    is_first_reapro = models.BooleanField(default=True)


class Client(models.Model):
    idClient = models.TextField(blank=False, default="")
    prenom = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    ptsFidelite = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    compte = models.CharField(max_length=10, default="")
    promo = models.IntegerField(default=0)


class Produit(models.Model):
    codeProduit = models.CharField(max_length=200, primary_key=True)
    # codeProduitFournisseur = models.CharField(max_length=200)
    # nomFournisseur = models.CharField(max_length=200)
    familleProduit = models.CharField(max_length=200)
    descriptionProduit = models.CharField(max_length=200)
    quantiteMin = models.PositiveIntegerField(default=0)
    packaging = models.PositiveIntegerField(default=0)
    prix = models.PositiveIntegerField(default=0)
    exclusivite = models.CharField(max_length=10, default=0)
    promo = models.IntegerField(default=0)
    prixApres = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=0)


class Vente(models.Model):
    date = models.DateTimeField()
    prix = models.IntegerField()
    client = models.CharField(max_length=50)
    pointsFidelite = models.IntegerField()
    modePaiement = models.CharField(max_length=10)
    articles = models.ManyToManyField(Produit, through='ArticleVendu')


class ArticleVendu(models.Model):
    article = models.ForeignKey(Produit, on_delete=models.PROTECT)
    vente = models.ForeignKey(Vente, on_delete=models.PROTECT)
    quantite = models.IntegerField(null=True)


class Commande(models.Model):
    # Statut : reçu, en cours...
    date = models.DateTimeField(null=True)
    statut = models.CharField(max_length=20, default="En Cours")
    articles = models.ManyToManyField(Produit, through='ArticleCommande')


class ArticleCommande(models.Model):
    article = models.ForeignKey(Produit, on_delete=models.PROTECT)
    commande = models.ForeignKey(Commande, on_delete=models.PROTECT)
    quantite = models.IntegerField()

class CustomersProducts(models.Model):
    date = models.DateTimeField()
    idClient = models.TextField(blank=False, default="")
    codeProduit = models.CharField(max_length=200)
    quantite = models.IntegerField()
    promo = models.IntegerField(default=0)


