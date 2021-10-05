# Generated by Django 3.2.7 on 2021-10-05 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_app', '0006_auto_20211005_0540'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='wallet_address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='investments',
            name='uri',
            field=models.CharField(default='D23C99B8796F4642AA9019638258A6', max_length=50),
        ),
        migrations.AlterField(
            model_name='pop',
            name='uri',
            field=models.CharField(default='AC0228F49ACC447BA7CCEBF8330A85', max_length=50),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='coin_tpye',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='uri',
            field=models.CharField(default='54337D55A13B46F3B32ECB9FC89A25', max_length=50),
        ),
    ]
