# Generated by Django 2.1 on 2018-08-19 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openPW_REST_API', '0013_auto_20180819_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productexchange',
            name='is_verified',
        ),
    ]
