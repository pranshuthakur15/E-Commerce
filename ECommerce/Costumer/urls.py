from django.urls import path
# from .views import SignupAPIView,LoginAPIView,ProductListAPIView,ForgetPasswordAPIView,UpdatePasswordAPIView,AdminLoginAPIView,IndexAPIView, AboutUsAPIView, ContactUsAPIView
from .views import *
urlpatterns = [
    path('Costumer/signup/',SignupAPIView.as_view(),name='AddCostumer'),
    path('Costumer/login/',LoginAPIView.as_view(),name='login'),
    path('Costumer/logedIn/<int:costumer_id>/',AfterLoginAPIView.as_view(),name='loggedIn_index'),
    path('Costumer/forget_password/',ForgetPasswordAPIView.as_view(),name='forget_password'),
    path('Costumer/update_password/',UpdatePasswordAPIView.as_view(),name='update_password'),
    path('',ProductListAPIView.as_view(),name='index'),
    path('Costumer/about-us/', AboutUsAPIView.as_view(), name='about_us'),
    path('Costumer/about-us/<int:costumer_id>/', LoggedInAboutUsAPIView.as_view(), name='about_us_loggedIn'),
    path('Costumer/contact-us/<int:costumer_id>/', LoggedInContactUsAPIView.as_view(), name='contact_us_loggedIn'),
    path('Costumer/contact-us/', ContactUsAPIView.as_view(), name='contact_us'),
    path('Costumer/contact-us/messages/',ContactUsPageAPIView.as_view(),name='contact_us_messages'),
]

