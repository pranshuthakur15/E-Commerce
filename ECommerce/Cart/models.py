from django.db import models
from Costumer.models import CostumerModel
from Product.models import Product

class Cart(models.Model):
    #one cart can only be linked to one user
    user = models.OneToOneField(CostumerModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.first_name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"CartItem {self.pk} in {self.cart}"
