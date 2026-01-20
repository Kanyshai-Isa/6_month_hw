from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Review
from .serializers import (
    ProductListSerializer, ProductDetailSerializer,
    CategoryListSerializer, CetegoryDetailSerializer,
    ReviewListSerializer, ReviewDetailSerializer,
    ProductReviewSerializer, ProductValidateSerializer,
    CategoryValidateSerializer, ReviewValidateSerializer,
    )
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from common.permissions import IsOwner, IsAnonymous, CanEditWithin15Minutes, IsModerator, IsCustomAuthenticated
from rest_framework.permissions import SAFE_METHODS
from django.core.cache import cache


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
            return Response({
            'total': self.page.paginator.count,   #поменяли на total
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            })



class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    pagination_class =CustomPagination
    lookup_field = 'id'



class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CetegoryDetailSerializer
    lookup_field = 'id'    

    def post(self, request, *args, **kwargs):
        return Response


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all() 
    serializer_class = CategoryListSerializer
    pagination_class = CustomPagination



class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset  = Product.objects.all()
    serializer_class = ProductDetailSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.user.is_staff:
            if self.request.method == 'POST':
                return [IsCustomAuthenticated()]
            return [IsModerator()]

        if self.request.method in SAFE_METHODS:
            return [IsAnonymous()]
        if self.request.method in ['PUT', 'PATCH']:
            return [IsOwner(), CanEditWithin15Minutes()]
        if self.request.method == 'DELETE':
            return [IsOwner()]
        return [IsCustomAuthenticated()]


class ProductCreateListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsOwner | IsAnonymous]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer
        return ProductListSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.create(
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            price=serializer.validated_data['price'],
            category_id=serializer.validated_data['category_id'],
            owner = request.user
        )
        return Response(
            data=ProductDetailSerializer(product).data,
            status=status.HTTP_201_CREATED
        )
    
    def get(self, request, *args, **kwargs):
        cached_data = cache.get("product_list")
        if cached_data:
            print("Redis")
            return Response(data=cached_data, status=status.HTTP_200_OK)
        response = super().get(self, request, *args, **kwargs)
        print("Postgres")
        if response.data.get("total", 0) > 0:
            cache.set("product_list", response.data, timeout=300)
        return response