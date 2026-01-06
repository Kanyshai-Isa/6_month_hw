from django.urls import path
from . import views
from .constants import  LIST_CREATE, RETRIEVE_UPDATE_DESTROY

urlpatterns = [
    path('<int:id>/', views.ProductDetailAPIView.as_view()),
    path('categories/', views.CategoryListCreateAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('reviews/', views.ReviewViewSet.as_view(LIST_CREATE)),
    path('reviews/<int:id>/', views.ReviewViewSet.as_view(RETRIEVE_UPDATE_DESTROY)),
    path('', views.ProductCreateListAPIView.as_view())
    
]