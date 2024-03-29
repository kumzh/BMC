# Generated by Django 2.0.5 on 2019-04-20 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmc_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=20)),
                ('int_num', models.IntegerField()),
                ('int_info', models.CharField(max_length=50)),
                ('host_ip', models.GenericIPAddressField(unique=True)),
            ],
        ),
    ]
