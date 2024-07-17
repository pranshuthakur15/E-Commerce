from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Orders
from .serializers import OrderSerializer

class OrderCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)  # Assuming user is authenticated
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
