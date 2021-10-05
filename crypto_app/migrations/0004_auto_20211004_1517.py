# Generated by Django 3.2.7 on 2021-10-04 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_app', '0003_auto_20211004_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='investments',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='investments',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('pending', 'pending'), ('complete', 'completed')], default='pending', max_length=40),
        ),
        migrations.AlterField(
            model_name='investments',
            name='uri',
            field=models.CharField(default='CBA2690B05774F849DE530507C960B', max_length=50),
        ),
        migrations.AlterField(
            model_name='pop',
            name='uri',
            field=models.CharField(default='0B3C11497A024DB1BDF230660B35F5', max_length=50),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='uri',
            field=models.CharField(default='11C87692E79C46CE9159D4A1DF769E', max_length=50),
        ),
    ]
