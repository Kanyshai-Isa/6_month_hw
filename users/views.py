from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserRegisterSerializer, UserAuthSerializer,
    ConfirmCodeSerializer, UserSerializer,
    CustomTokenObtainPairSerializer
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from users.models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




class UserListAPIView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    


class AuthAPIView(CreateAPIView):
    serializer_class = UserAuthSerializer

    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)  
        if user is not None:
            token , created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status = status.HTTP_401_UNAUTHORIZED)




class RegistartionAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        birthdate = serializer.validated_data['birthdate']


        user = CustomUser.objects.create_user(   #не просто create!
            email=email,
            password=password,
            birthdate=birthdate,
            is_active=False, #сначала фолс, содать код и привязываете к пользователю
        )

        confirm = ConfirmCode.objects.create(user=user)
        return Response(data={'user_id':user.id, 'confirm_code': confirm.confirm_code}, status=status.HTTP_201_CREATED)
    


class ConfirmAPIView(CreateAPIView):
    serializer_class = ConfirmCodeSerializer

    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        confirm_code = serializer.validated_data['confirm_code']

        try:
            code_obj = ConfirmCode.objects.get(confirm_code=confirm_code)
        except ConfirmCode.DoesNotExist:
            return Response ({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = code_obj.user
        user.is_active = True
        user.save()


        return Response(data={'user_id':user.id}, status=status.HTTP_200_OK)



# @api_view(['POST'])
# def authorization_api_view(request):
#     serializer = UserAuthSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)

#     username = serializer.validated_data['username']
#     password = serializer.validated_data['password']

#     user = authenticate(username=username, password=password)   #user или None
#     if user is not None:
#         token , created = Token.objects.get_or_create(user=user)
#         return Response(data={'key': token.key})
#     return RecursionError(status = status.HTTP_401_UNAUTHORIZED)



# @api_view(['POST'])
# def registration_api_view(request):
#     serializer = UserRegisterSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)

#     username = serializer.validated_data['username']
#     password = serializer.validated_data['password']


#     user = User.objects.create_user(   #не просто create!
#         username=username,
#         password=password,
#         is_active=False, #сначала фолс, содать код и привязываете к пользователю
#     )

#     confirm = ConfirmCode.objects.create(user=user)
#     return Response(data={'user_id':user.id, 'confirm_code': confirm.confirm_code}, status=status.HTTP_201_CREATED)



# @api_view(['POST'])
# def confirm_code_api_view(request):
#     serializer = ConfirmCodeSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)

#     confirm_code = serializer.validated_data['confirm_code']

#     try:
#         code_obj = ConfirmCode.objects.get(confirm_code=confirm_code)
#     except ConfirmCode.DoesNotExist:
#         return Response ({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
    
#     user = code_obj.user
#     user.is_active = True
#     user.save()


#     return Response(data={'user_id':user.id}, status=status.HTTP_200_OK)
