# Generated by Django 2.0.5 on 2019-05-11 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_auto_20190511_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='to_mail',
            name='to_mail',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]