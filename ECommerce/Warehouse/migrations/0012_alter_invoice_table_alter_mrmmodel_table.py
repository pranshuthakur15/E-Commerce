# Generated by Django 5.0.4 on 2024-05-07 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Warehouse', '0011_invoice_mrmmodel'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='invoice',
            table='Invoice',
        ),
        migrations.AlterModelTable(
            name='mrmmodel',
            table='MRMModel',
        ),
    ]
