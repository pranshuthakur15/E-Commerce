# Create your views here.
from django.shortcuts import render


# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import CostumerModel
from .serializers import CostumerSerializer
import random
from django.db import models
from .models import CostumerModel
import datetime
from django.utils import timezone
from rest_framework.renderers import TemplateHTMLRenderer
from django.template.response import TemplateResponse
from Product.models import Product
from Costumer.models import CostumerModel
from Cart.models import Cart,CartItem
from django.core.paginator import Paginator

from django.contrib import messages

class SignupAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Costumer/signup_form.html'
    def get(self, request):
        return TemplateResponse(request, self.template_name)
  
    def post(self, request):
       # Handle POST request, process signup data
        serializer = CostumerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            first_name = serializer.validated_data['first_name']
            messages.success(request,f"Welcome {first_name}")
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            address = serializer.validated_data['address']
            mobile = serializer.validated_data['mobile']


            send_mail(
               subject='SignUp Confirmation',
               message=f"Hello {first_name} {last_name} Your account has been created here is the information you have entered: Name: {first_name},Address: {address},Mobile Number: {mobile}",
               from_email="pranshu@skylabstech.com",
               recipient_list=[email],
               fail_silently=False)
            
            return TemplateResponse(request, 'Costumer/signup_confirmation.html', {'customer_data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
   

class LoginAPIView(APIView):
    def get(self, request):
        return render(request, 'Costumer/login.html')

    def post(self, request):
       # Handle POST request, process login data
        email = request.data.get('email')
        password = request.data.get('password')
        #To display the product by id and which have display filter True
        products = Product.objects.filter(display=True).order_by('id')
        paginator = Paginator(products, 9)  # Display 9 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        user = CostumerModel.objects.filter(email=email, password=password).first()
        if user:
            first_name = user.first_name
            messages.success(request,f"Welcome back {first_name}")
            cart = Cart.objects.filter(user=user).first()
            if cart:
                total = 0
                for item in cart.items.all():
                    item.subtotal = item.quantity
                    total += item.subtotal
                cart_items_count = total
            else:
                cart_items_count = 0
            return TemplateResponse(request, 'Pages/loggedIn_index.html', {'costumer': user, 'cart_items_count': cart_items_count, 'page_obj': page_obj})
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class AfterLoginAPIView(APIView):
    def get(self, request, costumer_id):
        costumer = CostumerModel.objects.get(pk= costumer_id)
        products = Product.objects.filter(display=True).order_by('id')
        paginator = Paginator(products, 12)  # Display 12 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        first_name = costumer.first_name
        costumer_id = costumer.pk

        cart = Cart.objects.filter(user=costumer).first()
        total=0
        for item in cart.items.all():
            item.subtotal = item.quantity 
            total += item.subtotal
        cart_items_count = total

        return TemplateResponse(request, 'Pages/loggedIn_index.html',{'costumer':costumer,'cart_items_count':cart_items_count, 'page_obj': page_obj})


class ForgetPasswordAPIView(APIView):
    def get(self, request):
        return render(request, 'Costumer/forget_password.html')
    def post(self, request):
       # Handle POST request, process forget password data
        email = request.data.get('email')
        user = CostumerModel.objects.filter(email=email).first()
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
           return TemplateResponse(request, 'Costumer/otp_sent.html')
        return Response({"message": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
   
class UpdatePasswordAPIView(APIView):
    def get(self, request):
        return render(request, 'Costumer/reset_password.html')
    def post(self, request):
       # Handle POST request, process update password data
       email = request.data.get('email')
       otp = request.data.get('otp')
       new_password = request.data.get('new_password')
       confirm_password = request.data.get('confirm_password')
       user = CostumerModel.objects.filter(email=email, otp=otp).first()
       time_difference = timezone.now() - user.otp_created_at
       if time_difference.total_seconds() > 300:  # 5 minutes
               return Response({"message": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
       if new_password != confirm_password:
           return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
       # Check OTP validity (for simplicity, after OTP is sent successfully)
       # Update password for the user
       if user:
           user.password = new_password
           user.save()
           return TemplateResponse(request, 'Costumer/password_reset_confirmation.html')
       return Response({"message": "Invalid OTP or Email"}, status=status.HTTP_404_NOT_FOUND)




class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(display=True).order_by('id')
        paginator = Paginator(products, 12)  # Display 12 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Pages/index.html', {'page_obj': page_obj})



class AboutUsAPIView(APIView):
    def get(self, request):
        return TemplateResponse(request, 'Pages/aboutUs.html')

  
    
class LoggedInAboutUsAPIView(APIView):
    def get(self, request,costumer_id):
        costumer = CostumerModel.objects.get(pk=costumer_id)
        return TemplateResponse(request, 'Pages/aboutUs_loggedIn.html',{'costumer':costumer})

class ContactUsAPIView(APIView):
    def get(self, request):
        return TemplateResponse(request, 'Pages/contactUs.html')



class LoggedInContactUsAPIView(APIView):
    def get(self, request, costumer_id):
        costumer = CostumerModel.objects.get(pk=costumer_id)
        return TemplateResponse(request, 'Pages/contactUs_loggedIn.html', {'costumer': costumer})

    def post(self, request, costumer_id):
        costumer = CostumerModel.objects.get(pk=costumer_id)
        costumer_email = costumer.email
        products = Product.objects.filter(display=True).order_by('id')
        paginator = Paginator(products, 12)  # Display 12 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        message = request.POST.get('message', '')  # Get the message from POST data
        send_mail(
            'Customer Inquiry',  # Subject
            message,  # Message
            costumer_email,  # From email
            ['pranshu@skylabstech.com'],  # To email(s)
            fail_silently=False,  # Raise exceptions on failure
        )
        return TemplateResponse(request, 'Pages/loggedIn_index.html', {'costumer': costumer , 'page_obj': page_obj})


class ContactUsPageAPIView(APIView):
    def get(self, request):
        return TemplateResponse(request, 'Costumer/ContactUs.html')
    
    def post(self, request):
        email = request.data.get('email')
        message = request.data.get('message')
        products = Product.objects.filter(display=True).order_by('id')
        paginator = Paginator(products, 12)  # Display 12 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        send_mail(
            subject='Customer Inquiry',  
            message=message,  
            from_email=email,  
            recipient_list=['pranshu@skylabstech.com'],  
            fail_silently=False,  
        )
        return TemplateResponse(request, 'Pages/index.html',{'page_obj': page_obj})
    