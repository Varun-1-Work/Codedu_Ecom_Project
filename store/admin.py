from django.contrib import admin
from .models import Category, Product
from django.contrib.auth.models import Group, User

# Register your models here.
admin.site.unregister(Group)
admin.site.unregister(User)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'trending')
    prepopulated_fields={'slug':('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'selling_price', 'status', 'trending')
    prepopulated_fields={'slug':('name',)}    


admin.site.register(Category)
admin.site.register(Product)

