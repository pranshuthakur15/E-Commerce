
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import StockSerializer
from Category.models import Category
from Sub_Category.models import SubCategory
from Product.models import Product
from .models import Stock
from django.template.loader import render_to_string
from django.http import HttpResponse
from Warehouse.models import AdminModel
from django.template.response import TemplateResponse

# Create your views here.
class AddStocksAPIView(APIView):
    def get(self, request,admin_id):
        categories = Category.objects.all()  # Fetch all categories
        subcategories = SubCategory.objects.all()  # Fetch all subcategories
        products = Product.objects.filter(display=True).order_by('id')  # Fetch all products
        admin=AdminModel.objects.get(id= admin_id)
        return render(request, 'Stock/add_stocks.html' ,{'categories': categories, 'subcategories': subcategories , 'page_obj': products,'admin':admin})

    def post(self,request,admin_id):
        serializer = StockSerializer(data = request.data)
        admin = AdminModel.objects.get(id=admin_id)
        if serializer.is_valid():
            product = serializer.validated_data.get('product')
            product = Product.objects.get(id=product.pk)
            hsn_code = product.hsn_code
            serializer.save(hsn_code=hsn_code)
            return TemplateResponse(request, 'Admin/adminLoggedIn.html',{'admin':admin})
        else:
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
class UpdateStockAPIView(APIView):
    def get(self, request, admin_id,stock_id):
        stock = get_object_or_404(Stock, pk=stock_id)
        admin = AdminModel.objects.get(id=admin_id)
        categories = Category.objects.all()  # Fetch all categories
        subcategories = SubCategory.objects.all()  # Fetch all subcategories
        products = Product.objects.filter(display=True).order_by('id') # Fetch all products
        serializer = StockSerializer(stock)
        return render(request, 'Stock/update_stocks.html' ,{'admin':admin,'categories': categories, 'subcategories': subcategories , 'page_obj': products,'stock': stock})


    def patch(self, request,admin_id,stock_id):
        stock = get_object_or_404(Stock, pk=stock_id)
        admin = AdminModel.objects.get(id=admin_id)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return TemplateResponse(request, 'Admin/adminLoggedIn.html',{'admin':admin})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListStocksAPIView(APIView):
    def get(self, request,admin_id):
        stocks = Stock.objects.all()
        # serializer = StockSerializer(stocks, many=True)
        categories = Category.objects.all()  # Fetch all categories
        subcategories = SubCategory.objects.all()  # Fetch all subcategories
        products = Product.objects.filter(display=True).order_by('id')  # Fetch all products
        admin = AdminModel.objects.get(id=admin_id) #
        html_content = render_to_string('Stock/list_stocks.html', {'stocks': stocks,'admin':admin})
        return HttpResponse(html_content)