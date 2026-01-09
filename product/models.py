from django.db import models
from django.db.models import Avg
from users.models import CustomUser
from common.models import BaseModel

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def product_count(self):
        return self.product_set.count()


class Product(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def review_list(self):
        return [review.text for review in self.reviews.all()] 
    
    def rating(self):
        return self.reviews.aggregate(avg=Avg('stars'))['avg']


    
STARS = (
    (i, '*' * i) for i in range(1,6)
)
class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    stars = models.IntegerField(choices=STARS, default=0, null=True, blank=True)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='reviews',
                                null=True,
                                blank=True)
    def __str__(self):
        return (self.text)
    