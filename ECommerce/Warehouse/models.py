from django.db import models
from Category.models import Category
from Product.models import Product
from Sub_Category.models import SubCategory
import uuid
from django.utils.translation import gettext_lazy as _

# Create your models here.
class AdminModel(models.Model):
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
    
    class Meta:
       db_table = "admin"
        

class VendorModel(models.Model):
    vendor_name = models.CharField(max_length=120)
    vendor_email = models.EmailField(unique=True)
    vendor_mobile = models.CharField(max_length=12,unique=True)
    vendor_address = models.CharField(max_length=120)
    vendor_password = models.CharField(max_length=120)
    vendor_confirmpassword = models.CharField(max_length=120)
    vendor_otp = models.CharField(max_length=8,default=0)
    vendor_otp_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.vendor_name

    class Meta:
       db_table = "vendor"


class PurchaseOrder(models.Model):
    STATUS_CHOICES =(
        ('ACTIVE', 'Active'),
        ('PENDING', 'Pending'),
        ('REJECTED', 'Rejected'),
    )
    po = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    po_id = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE,default=1)
    MRMcreated = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.po_id)+" ••• "+self.vendor.vendor_name+" ••• "+str(self.status)+" ••• "+str(self.created_at)
    
    class Meta:
       db_table = "purchase_order"

class OrderItem(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,default=0)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} - {self.order.vendor.vendor_name}"
    
    class Meta:
       db_table = "order_item"

class MRMmodel(models.Model):
    MODE_OF_PAYMENT_CHOICES = (
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('NEFT', 'NEFT'),
        ('RTGS', 'RTGS'),
        ('UPI','UPI'),
        )
    purchase_order = models.OneToOneField(PurchaseOrder, on_delete=models.CASCADE)
    invoice_date = models.DateField(_("Invoice Date"), auto_now_add=True)
    mode_of_payment = models.CharField(max_length=100, choices=MODE_OF_PAYMENT_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.purchase_order.vendor.vendor_name} - {self.purchase_order.po_id} - Rs.{self.total_amount} - {self.mode_of_payment}"
    
    class Meta:
       db_table = "MRMmodel"

class MRMItem(models.Model):
    mrm_model = models.ForeignKey(MRMmodel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_offered = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_offered = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_offered = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} -  - {self.quantity_offered}"
    
    class Meta:
       db_table = "MRMitems"