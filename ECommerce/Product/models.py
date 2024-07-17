from django.db import models
from Category.models import Category
from Sub_Category.models import SubCategory

class Product(models.Model):
    name = models.CharField(max_length=100)
    display = models.BooleanField(default=True)
    images = models.JSONField(default=list)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hsn_code = models.CharField(max_length=10,default=0)

    def __str__(self):
        return self.name

    class Meta:
       db_table = 'product' 