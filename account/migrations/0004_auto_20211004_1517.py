# Generated by Django 3.2.7 on 2021-10-04 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20211004_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='uri',
            field=models.CharField(blank=True, default='33B3D79036', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='wallet_id',
            field=models.CharField(default='262A07FE7A', max_length=50, unique=True),
        ),
    ]
