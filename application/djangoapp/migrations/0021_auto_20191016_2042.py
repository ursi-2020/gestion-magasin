# Generated by Django 2.2.6 on 2019-10-16 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0020_auto_20191016_1836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vente',
            name='articles',
        ),
        migrations.AddField(
            model_name='article',
            name='ventes',
            field=models.ManyToManyField(to='djangoapp.Vente'),
        ),
    ]
