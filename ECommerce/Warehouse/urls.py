from django.urls import path
from .views import *

urlpatterns = [
    path('vendor/signup/',SignupAPIView.as_view(),name='AddVendor'),
    path('vendor/login/',LoginAPIView.as_view(),name='vendor_Login'),
    path('vendor/loggedIn_vendor/<int:vendor_id>/',AfterLoginAPIView.as_view(),name='loggedIn_vendor'),
    path('vendor/forget_password/',ForgetPasswordAPIView.as_view(),name='forget_password'),
    path('vendor/update_password/',UpdatePasswordAPIView.as_view(),name='update_password'),
    path('admin/purchaseOrder/<int:admin_id>/',PurchaseOrderAPIView.as_view(),name='purchaseOrder'),
    path('admin/',AdminLoginAPIView.as_view(),name='adminLogin'),
    path('admin/logedIn/<int:admin_id>/',AfterAdminLoginAPIView.as_view(),name='loggedIn_admin'),
    path('admin/VendorList/<int:admin_id>/',ListVendorAPIView.as_view(),name='vendorList'),
    path('admin/VendorDetails/<int:admin_id>/<int:vendor_id>/',VendorDetailsAPIView.as_view(),name='vendorDetails'),
    path('admin/VendorDetails/purchaseOrderList/<int:admin_id>/<int:vendor_id>/',PurchaseOrderList.as_view(),name='purchaseOrderList'),
    path('admin/VendorDetails/purchaseOrderList/listOrderItems/<int:admin_id>/<int:vendor_id>/<int:po_id>/',ListOrderItems.as_view(),name='POlist'),
    path('admin/MaterialRequestList/<int:admin_id>/',MRMList.as_view(),name='materialRequestList'),
    path('admin/MaterialRequest/<int:admin_id>/<int:po_id>/',MRMInvoiceAPIView.as_view(),name='materialRequest'),

]

