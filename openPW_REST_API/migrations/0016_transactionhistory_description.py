# Generated by Django 2.1 on 2018-08-19 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openPW_REST_API', '0015_salesrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistory',
            name='description',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
    ]
