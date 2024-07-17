from rest_framework import serializers
from .models import CostumerModel




class CostumerSerializer(serializers.ModelSerializer):
   class Meta:
       model = CostumerModel
       fields = '__all__'


   def validate_email(self, value):
       # Check if the email address already exists in the database
       if CostumerModel.objects.filter(email=value).exists():
           raise serializers.ValidationError("This email address is already in use.")
       return value
   def validate_mobile(self, value):
       if CostumerModel.objects.filter(mobile=value).exists():
           raise serializers.ValidationError("This mobile number is already in use.")
       return value
       