# Generated by Django 5.0.4 on 2024-05-03 11:52

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Product', '0004_product_display'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', models.CharField(max_length=12, unique=True)),
                ('address', models.CharField(max_length=120)),
                ('password', models.CharField(max_length=120)),
                ('confirmpassword', models.CharField(max_length=120)),
                ('otp', models.CharField(default=0, max_length=8)),
                ('otp_created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'admin',
            },
        ),
        migrations.CreateModel(
            name='VendorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=120)),
                ('vendor_email', models.EmailField(max_length=254, unique=True)),
                ('vendor_mobile', models.CharField(max_length=12, unique=True)),
                ('vendor_address', models.CharField(max_length=120)),
                ('vendor_password', models.CharField(max_length=120)),
                ('vendor_confirmpassword', models.CharField(max_length=120)),
                ('vendor_otp', models.CharField(default=0, max_length=8)),
                ('vendor_otp_created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'vendor',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item_discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('quantity', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('po_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('PENDING', 'Pending'), ('REJECTED', 'Rejected')], default='ACTIVE', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('products', models.ManyToManyField(through='Warehouse.OrderItem', to='Product.product')),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Warehouse.purchaseorder'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Warehouse.vendormodel'),
        ),
    ]
