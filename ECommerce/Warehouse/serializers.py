from rest_framework import serializers
from .models import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = '__all__'

from rest_framework import serializers
from .models import PurchaseOrder, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'item_price', 'quantity']
        extra_kwargs = {'product': {'required': True},
                        'item_price': {'required': True},
                        'quantity': {'required': True}}

class PurchaseOrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = ['po','po_id', 'status', 'created_at', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=purchase_order, **item_data)
        return purchase_order


