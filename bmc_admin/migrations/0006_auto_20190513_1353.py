# Generated by Django 2.0.5 on 2019-05-13 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmc_admin', '0005_host_info_cpu_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host_info',
            name='cpu_info',
            field=models.CharField(max_length=70),
        ),
    ]