# Generated by Django 2.0.5 on 2018-08-17 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bCoreRiskApp', '0011_auto_20180817_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riskfield',
            name='field_date',
            field=models.DateField(null=True),
        ),
    ]
