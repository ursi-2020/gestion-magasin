# Generated by Django 2.2.6 on 2019-10-20 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0029_auto_20191020_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlevendu',
            name='quantite',
            field=models.IntegerField(null=True),
        ),
    ]
