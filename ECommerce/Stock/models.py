from django.db import models

# Create your models here.
from django.db import models
from Product.models import Product,Category,SubCategory

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    hsn_code = models.CharField(max_length=10,default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    class Meta:
       db_table = 'stocks' 