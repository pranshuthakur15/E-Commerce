from django.db import models

# Create your models here.
class CostumerModel(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=12,unique=True)
    address = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    confirmpassword = models.CharField(max_length=120)
    otp = models.CharField(max_length=8,default=0)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name
        
        

    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    class Meta:
       db_table = "costumers"