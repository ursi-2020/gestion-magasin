# Generated by Django 2.2.6 on 2019-11-21 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0036_auto_20191112_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalinfo',
            name='is_first_reapro',
            field=models.BooleanField(default=True),
        ),
    ]