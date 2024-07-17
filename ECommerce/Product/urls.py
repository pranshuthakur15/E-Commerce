from django.urls import path
from .views import *

urlpatterns = [
    path('addProduct/<int:admin_id>/',AddProductAPIView.as_view(),name='AddProduct'),
    path('all-products/', AllProductsAPIView.as_view(), name='all_products'),
    path('list_products/<int:admin_id>/', LoggedInAllProductsAdminAPIView.as_view(), name='list_products'),
    # path('products-by-category/<int:category_id>/', ProductsByCategoryAPIView.as_view(), name='products_by_category'),
    path('search/',ProductsByCategoryAPIView.as_view(),name='search'),
    path('loggedIn-all-products/<int:costumer_id>/',LoggedInAllProductsAPIView.as_view(),name='logged_in_all_products'),
    path('json', FetchAndStoreData.as_view(), name='json'),
]
