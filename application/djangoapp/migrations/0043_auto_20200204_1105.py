# Generated by Django 3.0.2 on 2020-02-04 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0042_auto_20200204_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customersproducts',
            name='date',
        ),
        migrations.RemoveField(
            model_name='customersproducts',
            name='quantite',
        ),
        migrations.AlterField(
            model_name='customersproducts',
            name='codeProduit',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='customersproducts',
            name='idClient',
            field=models.TextField(),
        ),
    ]
