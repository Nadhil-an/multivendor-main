from django.db import models
from vendor.models import Vendor

# Create your models here.
class Category(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100)
    description = models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        unique_together = ('vendor', 'category_name','slug')

    def __str__(self):
        return self.category_name
    
    def clean(self):
        self.category_name = self.category_name.capitalize()

    
class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems')
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250,blank=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='foodimages')
    is_available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('category','food_title')

    def __str__(self):
        return self.food_title 
    
    def clean(self):
        self.food_title = self.food_title.capitalize()

    

