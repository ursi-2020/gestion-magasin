# Generated by Django 2.2.5 on 2019-09-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0009_globalinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalinfo',
            name='catalogue_is_down',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='globalinfo',
            name='crm_is_down',
            field=models.BooleanField(default=False),
        ),
    ]
