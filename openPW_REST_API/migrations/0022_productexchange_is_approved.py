# Generated by Django 2.1 on 2018-08-25 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openPW_REST_API', '0021_auto_20180822_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='productexchange',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
