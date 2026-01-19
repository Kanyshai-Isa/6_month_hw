from rest_framework import serializers
from users.models import CustomUser
from rest_framework.exceptions import ValidationError
from .models import ConfirmCode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email

        if user.birthdate:
            token["birthdate"] = user.birthdate.date().isoformat()
        else:
            token["birthdate"] = None

        return token



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField()

class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False)
    birthdate = serializers.DateField(required=False)

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            birthdate=validated_data.get('birthdate'),
        )

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("CustomUser already exists!")
        return email

    

class ConfirmCodeSerializer(serializers.Serializer):
    confirm_code = serializers.CharField(max_length=6)

    def validate_code(self,confirm_code):
        try:
              ConfirmCode.objects.get(confirm_code=confirm_code)
              return confirm_code
        except ConfirmCode.DoesNotExist:
            raise ValidationError('This code does not exist')

