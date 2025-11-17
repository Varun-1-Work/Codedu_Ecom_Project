from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='category/', blank=True, null=True)

    # 0 = Show, 1 = Hide
    status = models.BooleanField(default=False, help_text="0=default,1=Hidden")

    # Trending category
    trending = models.BooleanField(default=False, help_text="0=default,1=Hidden")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)
    small_description = models.CharField(max_length=250, blank=True)
    quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    
    original_price = models.FloatField()
    selling_price = models.FloatField()
    
    # 0 = Show, 1 = Hidden
    status = models.BooleanField(default=False, help_text="0=default,1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default,1=Hidden")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
