# Generated by Django 5.0.4 on 2024-04-15 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0002_stock_cost_price_stock_discount_stock_hsn_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
