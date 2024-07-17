# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib import messages
from .serializers import *
import random
from .models import *
from django.utils import timezone
from rest_framework.renderers import TemplateHTMLRenderer
from django.template.response import TemplateResponse
from Product.models import Product
from Costumer.models import CostumerModel
from Category.models import Category
from Sub_Category.models import SubCategory
from Stock.models import Stock
from .forms import OrderItemForm
from django.db import transaction

class SignupAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Vendor/signup_form.html'
    def get(self, request):
        return TemplateResponse(request, self.template_name)
  
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            vendor_name = serializer.validated_data['vendor_name']
            vendor_email = serializer.validated_data['vendor_email']
            vendor_address = serializer.validated_data['vendor_address']
            vendor_mobile = serializer.validated_data['vendor_mobile']

            send_mail(
               subject='SignUp Confirmation',
               message=f"Hello {vendor_name}  Your account has been created here is the information you have entered: Name: {vendor_name},Address: {vendor_address},Mobile Number: {vendor_mobile}",
               from_email="pranshu@skylabstech.com",
               recipient_list=[vendor_email],
               fail_silently=False)
            
            return TemplateResponse(request, 'Vendor/Vendor_login_success.html', {'vendor': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
   

class LoginAPIView(APIView):
    def get(self, request):
        return render(request, 'Vendor/login.html')

    def post(self, request):
        email = request.data.get('vendor_email')
        password = request.data.get('vendor_password')
        vendor = VendorModel.objects.filter(vendor_email=email, vendor_password=password).first()
        if vendor:
            messages.success(request,"Welcome back Vendor")
            return TemplateResponse(request, 'Vendor/Vendor_login_success.html', {'vendor': vendor})
        else:
            messages.error(request,"Invalid credentials")
            return render(request, 'Vendor/login.html')
        
        
    
class AfterLoginAPIView(APIView):
    def get(self, request, vendor_id):
        vendor = VendorModel.objects.get(id=vendor_id)
        return TemplateResponse(request, 'Vendor/Vendor_login_success.html',{'vendor':vendor})


class ListVendorAPIView(APIView):
    def get(self, request,admin_id):
        admin = AdminModel.objects.get(id=admin_id)
        vendors = VendorModel.objects.all()
        return TemplateResponse(request, 'Vendor/vendorList.html',{'admin':admin,'vendors': vendors})
    
    def post(self,request,admin_id,vendor_id):
        vendor=VendorModel.objects.get(id=vendor_id)
        admin = AdminModel.objects.get(id=admin_id)
        return TemplateResponse(request, 'Vendor/vendorDetails.html',{'vendor':vendor,'admin':admin})
        
class VendorDetailsAPIView(APIView):
    def get(self,request,admin_id,vendor_id):
        admin=AdminModel.objects.get(id=admin_id)
        vendor=VendorModel.objects.get(id=vendor_id)
        return TemplateResponse(request, 'Vendor/vendorDetails.html',{'vendor':vendor,'admin':admin})

class ForgetPasswordAPIView(APIView):
    def get(self, request):
        return render(request, 'Vendor/forget_password.html')
    def post(self, request):
       # Handle POST request, process forget password data
        email = request.data.get('email')
        user = VendorModel.objects.filter(email=email).first()
        if user:
           otp = random.randint(100000, 999999)
           user.otp = otp
           user.otp_created_at = timezone.now()
           user.save()
           send_mail(
               subject='Password Reset OTP',
               message=f'Your OTP is: {otp}',
               from_email='pranshu@skylabstech.com',
               recipient_list=[email],
               fail_silently=False)
           return TemplateResponse(request, 'Vendor/otp_sent.html')
        return Response({"message": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
   
class UpdatePasswordAPIView(APIView):
    def get(self, request):
        return render(request, 'Vendor/reset_password.html')
    def post(self, request):
       email = request.data.get('email')
       otp = request.data.get('otp')
       new_password = request.data.get('new_password')
       confirm_password = request.data.get('confirm_password')
       user = VendorModel.objects.filter(email=email, otp=otp).first()
       time_difference = timezone.now() - user.otp_created_at
       if time_difference.total_seconds() > 300:  # 5 minutes
               return Response({"message": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
       if new_password != confirm_password:
           return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

       # Update password for the user
       if user:
           user.password = new_password
           user.save()
           return TemplateResponse(request, 'Vendor/password_reset_confirmation.html')
       return Response({"message": "Invalid OTP or Email"}, status=status.HTTP_404_NOT_FOUND)


class AdminLoginAPIView(APIView):
    def get(self, request):
        return render(request, 'Admin/admin_login.html')
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        # Validate email and password
        if not email or not password:
            messages.warning(request, 'Please email and password')
            return render(request, 'Admin/admin_login.html')
        
        # Authenticate user
        user = AdminModel.objects.filter(email=email, password=password).first()
        if user:
            messages.success(request, 'Welcome Admin!')
            admin = AdminModel.objects.get(email= email)
            products = Product.objects.filter(display=True).order_by('id')
            vendor= VendorModel.objects.all() # Fetch all vendor
            sub_category = SubCategory.objects.all()
            category = Category.objects.all()
            stocks = Stock.objects.all()
            return TemplateResponse(request, 'Admin/adminLoggedIn.html',{'admin':user,'page_obj': products,'vendor':vendor,'category':category,'subcategory':sub_category,'stocks':stocks})    
        else:
            messages.warning(request, 'Invalid email or password')
            return render(request, 'Admin/admin_login.html')

class AfterAdminLoginAPIView(APIView):
    def get(self, request, admin_id):
        admin = AdminModel.objects.get(pk= admin_id)
        products = Product.objects.filter(display=True).order_by('id')
        vendor= VendorModel.objects.all() # Fetch all vendor
        sub_category = SubCategory.objects.all()
        category = Category.objects.all()
        stocks = Stock.objects.all()
        return TemplateResponse(request, 'Admin/adminLoggedIn.html',{'admin':admin,'page_obj': products,'vendor':vendor,'category':category,'subcategory':sub_category,'stocks':stocks})





class PurchaseOrderAPIView(APIView):
    def get(self, request, admin_id):
       
        admin = AdminModel.objects.get(pk=admin_id)
        categories = Category.objects.all()
        products = Product.objects.filter(display=True).order_by('id')
        vendors = VendorModel.objects.all()
        return TemplateResponse(request,'PurchaseOrder/purchaseOrder.html', {'admin': admin, 'category': categories, 'products': products, 'vendors': vendors})
    def post(self, request, admin_id):
        # Create a new PurchaseOrder instance
        admin = AdminModel.objects.get(pk= admin_id)
        products = Product.objects.filter(display=True).order_by('id')
        vendor= VendorModel.objects.all() # Fetch all vendor
        sub_category = SubCategory.objects.all()
        category = Category.objects.all()
        stocks = Stock.objects.all()
        print("data", request.data)
        purchase_order = PurchaseOrder.objects.create(
            vendor_id=request.data.get('vendor'),
            po_id=request.data.get('po_id'),
            status=request.data.get('status')
        )
        serializers = PurchaseOrderSerializer(data=purchase_order)
        if serializers.is_valid():
            serializers.save()
        # Extract order items data from the request
        order_items = []
        seen_products = set()
        for key, value in request.data.items():
            if key.startswith('order_items'):
                index = key.split('[')[1].split(']')[0]  # Extract the index from the key
                product_id = request.data.get(f'order_items[{index}][product]')
                # Check if the product ID has already been seen
                if product_id not in seen_products:
                    item_data = {
                        'product': product_id,
                        'item_price': request.data.get(f'order_items[{index}][item_price]'),
                        'quantity': request.data.get(f'order_items[{index}][quantity]')
                    }
                    order_items.append(item_data)
                    seen_products.add(product_id)  # Add the product ID to the set of seen products

        print("Order items data:", order_items)

        # Iterate over each order item data and create OrderItem instances
        for item_data in order_items:
            if not item_data['item_price']:
                item_data['item_price'] = 0  # Set a default value
            form = OrderItemForm(item_data)
            if form.is_valid():
                # Assign the purchase order to the order item and save it
                order_item = form.save(commit=False)
                order_item.order = purchase_order
                order_item.save()
                print(order_item)
            else:
                messages.error(request,"INVALID PRODUCT")
        messages.success(request,"Purchase Order send successfully")
        return TemplateResponse(request, 'Admin/adminLoggedIn.html',{'admin':admin,'page_obj': products,'vendor':vendor,'category':category,'subcategory':sub_category,'stocks':stocks})

class PurchaseOrderList(APIView):
    def get(self, request,admin_id,vendor_id):
        admin = AdminModel.objects.get(pk=admin_id)
        vendor=VendorModel.objects.get(pk=vendor_id)
        purchaseorder = PurchaseOrder.objects.filter(vendor=vendor)
        categories = Category.objects.all()
        products = Product.objects.filter(display=True).order_by('id')
        return TemplateResponse(request,'PurchaseOrder/purchaseOrderList.html', {'admin': admin,'vendor':vendor, 'category': categories, 'products': products,'purchase_order':purchaseorder})
    
class ListOrderItems(APIView):
    def get(self, request,admin_id,vendor_id,po_id):
        admin = AdminModel.objects.get(pk=admin_id)
        vendor=VendorModel.objects.get(pk=vendor_id)
        purchaseorder = PurchaseOrder.objects.get(po_id=po_id)
        orderItems = OrderItem.objects.filter(order=purchaseorder)
        categories = Category.objects.all()
        products = Product.objects.filter(display=True).order_by('id')
        return TemplateResponse(request,'PurchaseOrder/listOrderItems.html', {'admin': admin, 'category': categories, 'products': products,'orderItems':orderItems})


class MRMList(APIView):
    def get(self, request,admin_id):
        admin=AdminModel.objects.get(id=admin_id)
        purchaseOrder = PurchaseOrder.objects.all()
        categories = Category.objects.all()
        products = Product.objects.filter(display=True).order_by('id')
        return TemplateResponse(request,'MaterialReciept/MaterialRecieptList.html', {'admin': admin, 'category': categories, 'products': products,'purchaseOrder':purchaseOrder})


class MRMInvoiceAPIView(APIView):
    def get(self, request,admin_id,po_id):
        admin = AdminModel.objects.get(pk=admin_id)
        purchaseorder = PurchaseOrder.objects.get(po_id=po_id)
        vendor=VendorModel.objects.get(pk=purchaseorder.vendor.pk)
        orderItems = OrderItem.objects.filter(order=purchaseorder)
        categories = Category.objects.all()
        modeOfPayment = MRMmodel.MODE_OF_PAYMENT_CHOICES
        products = Product.objects.filter(display=True).order_by('id')
        return TemplateResponse(request,'MaterialReciept/MaterialReciept.html', {'admin': admin, 'category': categories, 'products': products,'vendor':vendor,'purchase_order':purchaseorder,'modeOfPayment':modeOfPayment})
    
    def post(self, request, admin_id, po_id):
        admin = AdminModel.objects.get(pk=admin_id)
        purchase_order = PurchaseOrder.objects.get(po_id=po_id)
        mode_of_payment = request.data.get('mode_of_payment')
        subtotal = request.data.get('subtotal')

        # Validate mode of payment and subtotal
        if not mode_of_payment or not subtotal:
            return Response({"error": "Mode of payment and subtotal are required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and save MRM model
        try:
            with transaction.atomic():
                #If any exception occurs during the execution of the block,
                # the transaction is rolled back, and no changes are made to the database.
                mrm_model = MRMmodel.objects.create(
                    purchase_order=purchase_order,
                    mode_of_payment=mode_of_payment,
                    total_amount=subtotal
                )

                # Save MRM items
                for order_item in purchase_order.orderitem_set.all():
                    price_offered = request.data.get(f'price_offered_{order_item.id}')
                    discount_offered = request.data.get(f'discount_offered_{order_item.id}')
                    quantity_offered = request.data.get(f'quantity_offered_{order_item.id}')

                    MRMItem.objects.create(
                        mrm_model=mrm_model,
                        product=order_item.product,
                        price_offered=price_offered,
                        discount_offered=discount_offered,
                        quantity_offered=quantity_offered
                    )
            purchase_order.MRMcreated = True
            purchase_order.save()

            return Response({"success": "MRM created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)