from django.urls import path
from .views import CartDetailView, AddToCartAPIView, RemoveFromCartView

urlpatterns = [
    path('<int:costumer_id>/', CartDetailView.as_view(), name='cart'),
    path('add/<int:costumer_id>/<int:product_id>/', AddToCartAPIView.as_view(), name='add_to_cart'),
    path('remove/<int:costumer_id>/<int:item_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
]
