# Generated by Django 2.0.5 on 2019-05-15 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20190515_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitor',
            name='min_1',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='min_15',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='min_5',
            field=models.FloatField(null=True),
        ),
    ]