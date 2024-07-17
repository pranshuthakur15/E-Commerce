
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100,null=False)
    desc = models.TextField(max_length=300)
    

    def __str__(self):
        return self.name


    class Meta:
       db_table = 'category'