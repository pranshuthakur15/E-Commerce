from django.urls import path
from .views import AddStocksAPIView,UpdateStockAPIView,ListStocksAPIView

urlpatterns = [
    path('addStocks/<int:admin_id>/',AddStocksAPIView.as_view(),name='AddStocks'),
    path('update-stock/<int:admin_id>/<int:stock_id>/',UpdateStockAPIView.as_view(),name='UpdateStock'),
    path('list/<int:admin_id>/', ListStocksAPIView.as_view(), name='list_stocks'),
]
