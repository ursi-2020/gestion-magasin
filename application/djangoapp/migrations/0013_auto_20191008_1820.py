# Generated by Django 2.2.5 on 2019-10-08 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0012_auto_20190930_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='fidelityPoint',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
