# Generated by Django 3.2.7 on 2021-10-05 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_app', '0005_auto_20211004_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='pop',
            name='status',
            field=models.CharField(default='approved', max_length=40),
        ),
        migrations.AlterField(
            model_name='investments',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('pending', 'pending'), ('completed', 'completed')], default='inactive', max_length=40),
        ),
        migrations.AlterField(
            model_name='investments',
            name='uri',
            field=models.CharField(default='791FC907B59D40EAB7609B2B1A26D6', max_length=50),
        ),
        migrations.AlterField(
            model_name='pop',
            name='uri',
            field=models.CharField(default='22A91B5764F545DFB6F70BEECC076E', max_length=50),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='uri',
            field=models.CharField(default='61E94BDBA35B4AB3AC9AF5245A8258', max_length=50),
        ),
    ]
