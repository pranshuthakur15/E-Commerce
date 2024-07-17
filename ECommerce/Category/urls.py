from django.urls import path
from .views import AddCategoryAPIView

urlpatterns = [
    path('addCategory/<int:admin_id>/',AddCategoryAPIView.as_view(),name='AddCategory'),
]
