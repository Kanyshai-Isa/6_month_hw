from django.urls import path
from . import views

urlpatterns = [
    # path('registration/', views.registration_api_view),
    path('',views.UserListAPIView.as_view()),
    path('registration/', views.RegistartionAPIView.as_view()),
    path('authorization/', views.AuthAPIView.as_view()),
    path('confirm/', views.ConfirmAPIView.as_view()),
]

# path('authorization/', views.authorization_api_view),