# Generated by Django 2.2.5 on 2019-09-29 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0008_auto_20190927_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products_last_update', models.DateTimeField(null=True)),
                ('customers_last_update', models.DateTimeField(null=True)),
            ],
        ),
    ]
