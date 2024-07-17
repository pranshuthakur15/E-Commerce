from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import ProductSerializer
from Category.models import Category
from Sub_Category.models import SubCategory
from .models import Product
from Costumer.models import CostumerModel
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.response import TemplateResponse
from Warehouse.models import AdminModel
import requests
from Stock.models import Stock


# Create your views here.
class AddProductAPIView(APIView):
    def get(self, request,admin_id):
        categories = Category.objects.all()  # Fetch all categories
        subcategories = SubCategory.objects.all()
        admin = AdminModel.objects.get(id=admin_id)
        return render(request, 'Product/add_product.html', {'categories': categories, 'subcategories': subcategories,'admin':admin})

    def post(self,request,admin_id):
        serializer = ProductSerializer(data = request.data)
        admin = AdminModel.objects.get(id=admin_id)
        if serializer.is_valid():
            serializer.save()
            return TemplateResponse(request, 'Admin/adminLogedIn.html',{'admin':admin})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AllProductsAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(display=True).order_by('id')
        html_content = render_to_string('Product/all_product.html', {'products': products})
        return HttpResponse(html_content)
    

class LoggedInAllProductsAPIView(APIView):
    def get(self, request,costumer_id):
        costumer = CostumerModel.objects.get(pk=costumer_id)
        products = Product.objects.filter(display=True).order_by('id')
        html_content = render_to_string('Product/loggedIn_all_products.html',{'costumer':costumer,'page_obj': products})
        return HttpResponse(html_content)
    

class LoggedInAllProductsAdminAPIView(APIView):
    def get(self, request,admin_id):
        admin = AdminModel.objects.get(pk=admin_id)
        products = Product.objects.filter(display=True).order_by('id')
        html_content = render_to_string('Product/all_productsAdmin.html',{'admin':admin,'page_obj': products})
        return HttpResponse(html_content)
         

class ProductsByCategoryAPIView(APIView):
    def get(self, request):
        query = request.GET.get('search')
        if query:
            results = Product.objects.filter(name__icontains=query)
        else:
            results= []
        return render(request, 'Pages/search_results.html', {'results': results, 'query': query})


#fetch json data from dummyjson API endpoint
class FetchAndStoreData(APIView):
    def get(self, request):
        try:
            # Make HTTP request to the API
            response = requests.get('https://dummyjson.com/products')
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            data = response.json()

            # Extract products from the response data an if its empty then a empty array is returned
            products = data.get('products', [])

            # Iterate over received products and create or update products
            for item in products:
                # Map category and subcategory identifiers to their corresponding objects
                category = item.get('category')
                subcategory = item.get('brand')

                # Retrieve or create category and subcategory objects
                category, _ = Category.objects.get_or_create(name=category)
                # If subcategory_id is provided, retrieve or create SubCategory object
                if subcategory:
                    subcategory, _ = SubCategory.objects.get_or_create(
                        name=subcategory, category=category)
                else:
                    subcategory = None

                # Create or update product
                product, created = Product.objects.update_or_create(
                    name=item.get('title'),
                    defaults={
                        'name': item.get('title'),
                        'category': category,
                        'subcategory': subcategory,
                        'description': item.get('description'),
                        'price': item.get('price'),
                        # Default value for hsn_code
                        'hsn_code': item.get('hsn_code', '8517'),
                        'images': item.get('images', []),
                    }
                )

                stock, _ = Stock.objects.get_or_create(
                    product=product,
                    defaults={
                        'category': category,
                        'subcategory': subcategory,
                        'quantity': item.get('stock', 1),
                        'cost_price': item.get('price', 0.0),
                        'selling_price': item.get('price', 0.0),
                        'discount': item.get('discountPercentage', 0.0),
                        'hsn_code': item.get('hsn_code', '8517'),
                    }
                )

            return Response("Data saved successfully", status=status.HTTP_201_CREATED)
        except requests.exceptions.RequestException as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
