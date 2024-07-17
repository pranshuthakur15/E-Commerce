from django import forms
from .models import *

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'item_price', 'quantity']

    def clean_item_price(self):
        item_price = self.cleaned_data['item_price']
        if item_price is None or item_price == '':
            return None
        return item_price


class MRMModelForm(forms.ModelForm):
    class Meta:
        model = MRMmodel
        fields = ['purchase_order', 'mode_of_payment', 'total_amount']

class MRMItem(forms.ModelForm):
    class Meta:
        model = MRMItem
        fields = ['product','price_offered','discount_offered','quantity_offered']