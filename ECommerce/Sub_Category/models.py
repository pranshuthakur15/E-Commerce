from django.db import models
from Category.models import Category

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
       db_table = 'subcategory' 