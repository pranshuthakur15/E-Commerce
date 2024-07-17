from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import CategorySerializer
from Warehouse.models import AdminModel
from django.template.response import TemplateResponse
# Create your views here.
class AddCategoryAPIView(APIView):
    def get(self,request,admin_id):
        admin = AdminModel.objects.get(id=admin_id)
        return render(request, 'Category/add_category.html',{'admin':admin})
    def post(self,request,admin_id):
        serializer = CategorySerializer(data = request.data)
        admin = AdminModel.objects.get(id=admin_id)
        if serializer.is_valid():
            serializer.save()
            return TemplateResponse(request, 'Admin/adminLogedIn.html',{'admin':admin})