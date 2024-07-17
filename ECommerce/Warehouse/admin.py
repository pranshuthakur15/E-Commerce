from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.


admin.site.register(VendorModel)

admin.site.register(AdminModel)

admin.site.register(PurchaseOrder)
admin.site.register(OrderItem)

admin.site.register(MRMmodel)
admin.site.register(MRMItem)