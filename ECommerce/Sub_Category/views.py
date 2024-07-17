
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import SubCategorySerializer
from Category.models import Category
from Warehouse.models import AdminModel
from .models import SubCategory
from django.template.response import TemplateResponse

# Create your views here.
class AddSubCategoryAPIView(APIView):
    def get(self, request,admin_id):
        categories = Category.objects.all()  # Fetch all categories
        admin = AdminModel.objects.get(id= admin_id)
        return render(request, 'Sub_category/add_subcategory.html', {'categories': categories,'admin':admin})

    def post(self,request,admin_id):
        serializer = SubCategorySerializer(data = request.data)
        admin = AdminModel.objects.get(id= admin_id)
        if serializer.is_valid():
            serializer.save()
            return TemplateResponse(request, 'Admin/adminLogedIn.html',{'admin':admin})