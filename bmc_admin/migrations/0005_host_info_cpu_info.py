# Generated by Django 2.0.5 on 2019-05-13 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmc_admin', '0004_auto_20190513_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='host_info',
            name='cpu_info',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]