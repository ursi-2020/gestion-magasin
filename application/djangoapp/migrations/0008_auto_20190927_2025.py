# Generated by Django 2.2.5 on 2019-09-27 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0007_auto_20190927_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='produit',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
