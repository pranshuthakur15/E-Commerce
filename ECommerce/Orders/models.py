from django.db import models
from Costumer.models import CostumerModel
from Product.models import Product

# Create your models here.
class Orders(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    Costumer = models.ForeignKey(CostumerModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField(max_length=120)
    mobile = models.CharField(max_length=12)
    address = models.CharField(max_length=120)
    order_date = models.DateTimeField(auto_now_add=True)
    order_time = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.Costumer.first_name} - {self.product.name}"