from rest_framework import serializers
from users.models import CustomUser
from rest_framework.exceptions import ValidationError
from .models import ConfirmCode


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField()

class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField()

    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
            raise ValidationError("CustomUser already exists! ")
        except CustomUser.DoesNotExist:
            return email

    

class ConfirmCodeSerializer(serializers.Serializer):
    confirm_code = serializers.CharField(max_length=6)

    def validate_code(self,confirm_code):
        try:
              ConfirmCode.objects.get(confirm_code=confirm_code)
              return confirm_code
        except ConfirmCode.DoesNotExist:
            raise ValidationError('This code does not exist')

