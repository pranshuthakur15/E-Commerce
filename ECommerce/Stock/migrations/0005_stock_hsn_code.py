# Generated by Django 5.0.4 on 2024-04-27 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0004_remove_stock_hsn_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='hsn_code',
            field=models.CharField(default=0, max_length=10),
        ),
    ]