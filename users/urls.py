from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from users.views import CustomTokenObtainPairView

urlpatterns = [
    # path('registration/', views.registration_api_view),
    path('',views.UserListAPIView.as_view()),
    path('registration/', views.RegistartionAPIView.as_view()),
    path('authorization/', views.AuthAPIView.as_view()),
    path('confirm/', views.ConfirmAPIView.as_view()),


    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('jwt/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

# path('authorization/', views.authorization_api_view),


