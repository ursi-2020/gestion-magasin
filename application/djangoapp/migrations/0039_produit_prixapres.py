# Generated by Django 2.2.7 on 2019-12-02 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0038_produit_promo'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='prixApres',
            field=models.IntegerField(default=0),
        ),
    ]