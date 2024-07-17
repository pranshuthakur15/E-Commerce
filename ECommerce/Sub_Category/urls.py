from django.urls import path
from .views import AddSubCategoryAPIView

urlpatterns = [
    path('addSubcategory/<int:admin_id>/',AddSubCategoryAPIView.as_view(),name='AddSubCategory'),
]
