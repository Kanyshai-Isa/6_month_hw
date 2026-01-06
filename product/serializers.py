from rest_framework import serializers
from .models import Product, Category, Review
from rest_framework.exceptions import ValidationError


class ProductReviewSerializer(serializers.ModelSerializer):
        rating = serializers.SerializerMethodField()  #для средней оценки

        class Meta:
                model = Product
                fields = ['title', 'reviews', 'rating', 'product_id']
                depth = 1

        def get_rating (self, obj):
                return obj.rating()

class ReviewDetailSerializer(serializers.ModelSerializer):
        class Meta:
                model = Review
                fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
        class Meta:
                model = Review
                fields = ['id', 'text', 'stars', 'product_id']


class CetegoryDetailSerializer(serializers.ModelSerializer):
        class Meta:
                model = Category
                fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
        product_count = serializers.SerializerMethodField()

        class Meta:
                model = Category
                fields = '__all__'

        def get_product_count(self, category):
                return category.product_count()



class ProductDetailSerializer(serializers.ModelSerializer):
        class Meta:
                model = Product
                fields = '__all__'


#дублирование
class ProductCreatetSerializer(serializers.ModelSerializer):
        reviews = serializers.SerializerMethodField()  #чтобы вывести наименования а не просто id

        class Meta:
                model = Product
                fields = ['id', 'title', 'price', 'description', 'reviews', 'category_id']


class ProductListSerializer(serializers.ModelSerializer):
        reviews = serializers.SerializerMethodField()  #чтобы вывести наименования а не просто id

        class Meta:
                model = Product
                fields = ['id', 'title', 'price', 'description', 'reviews', 'category_id']
                # fields = 'id title price description'.split
                # fields = '__all__'
                # exclude = ['id', 'price']
                # depth = 1
        
        def get_reviews (self, product):
                return product.review_list()


class ProductValidateSerializer(serializers.Serializer):
        title = serializers.CharField(min_length=1, max_length=255)
        description = serializers.CharField()
        price = serializers.IntegerField(min_value=1, max_value=200000)
        category_id = serializers.IntegerField()

        def validate_category_id(self, category_id):
                try:
                        Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                        raise ValidationError('category does not exist')
                return category_id
        
class CategoryValidateSerializer(serializers.Serializer):
        name = serializers.CharField(min_length=1, max_length=40)


class ReviewValidateSerializer(serializers.Serializer):
        text = serializers.CharField(min_length=1, max_length=255)
        stars = serializers.IntegerField(min_value=1, max_value=5)
        product_id = serializers.IntegerField()

        def validate_product_id(self, product_id):
                try:
                        Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                        raise ValidationError('product does not exist')
                return product_id