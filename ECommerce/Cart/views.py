from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from Product.models import Product
from Costumer.models import CostumerModel
from django.template.response import TemplateResponse
from .serializers import CartSerializer,CartItemSerializer
from django.core.paginator import Paginator
from django.contrib import messages

class AddToCartAPIView(APIView):
     def get(self, request, costumer_id,product_id):
        costumer = CostumerModel.objects.get(pk= costumer_id)
        products = Product.objects.filter(display=True).order_by('id')
        paginator = Paginator(products, 12)  # Display 12 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        first_name = costumer.first_name
        costumer_id = costumer.pk
        product = Product.objects.get(id=product_id)

        cart = Cart.objects.filter(user=costumer).first()
        total=0
        for item in cart.items.all():
            item.subtotal = item.quantity 
            total += item.subtotal
        cart_items_count = total

        return TemplateResponse(request, 'Pages/loggedIn_index.html',{'costumer':costumer,'cart_items_count':cart_items_count, 'page_obj': page_obj,'product_id':product_id, 'cart_items_count':cart_items_count})
         
     def post(self, request,product_id,costumer_id):
        costumer = CostumerModel.objects.get(pk=costumer_id)
        product = Product.objects.get(id=product_id)
        products = Product.objects.filter(display=True).order_by('id')
        paginator = Paginator(products, 9)  # Display 9 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        costumer = CostumerModel.objects.get(pk=costumer_id)
        first_name = costumer.first_name
        product_id = product.pk
        # Check if the product_id is provided and if provied does it exist in our db
        if not product:
            return Response({"message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        #This will Create our user Cart or retrieve the user's cart if already exists
        cart, created = Cart.objects.get_or_create(user=costumer)

        # Check if the product is already in the cart
        cart_item = cart.items.filter(product=product).first()
        if cart_item:
            # If item already exists, increase quantity
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"{product.name} has been added to your cart.")
        else:
            # If item doesn't exist, add it to the cart
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
            messages.success(request, f"{product.name} has been added to your cart.")
        total = 0
        # Here we Calculating the count of items in the cart
        for item in cart.items.all():
            item.subtotal = item.quantity 
            total += item.subtotal
        cart_items_count = total

        # now, Redirecting to the cart page with updated count
        return TemplateResponse(request, 'Pages/loggedIn_index.html',{'page_obj':page_obj ,'costumer':costumer, 'cart_items_count': cart_items_count})


class CartDetailView(APIView):
    def get(self, request,costumer_id):
        costumer = CostumerModel.objects.get(pk=costumer_id)
        cart = Cart.objects.filter(user=costumer).first()
        serializer = CartSerializer(cart)
        total = 0
        for item in cart.items.all():
            item.subtotal = item.quantity * item.product.price
            total += item.subtotal
        return TemplateResponse(request, 'Cart/cart_view.html', {'cart_items': cart.items.all(),'total': total ,'costumer':costumer})

class RemoveFromCartView(APIView):
    def post(self, request, item_id, costumer_id):
        costumer = CostumerModel.objects.get(pk=costumer_id)
        cart = Cart.objects.filter(user=costumer).first()
        total = 0
        try:
            item = CartItem.objects.get(id=item_id)
        except CartItem.DoesNotExist:
            messages.warning(request,"Products doest not exist")
            return TemplateResponse(request, 'Cart/cart_view.html', {'cart_items': cart.items.all(),'total': total ,'costumer':costumer })
            #now calculate the total
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
        
        # Recalculate total
        
        for item in cart.items.all():
            item.subtotal = item.quantity * item.product.price
            total += item.subtotal

        return TemplateResponse(request, 'Cart/cart_view.html', {'cart_items': cart.items.all(),'total': total ,'costumer':costumer })
