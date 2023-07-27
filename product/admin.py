from django.contrib import admin
from .models import Product, Cart, Category, CartItem, ProductImage, Rating
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register([Product, Cart, CartItem, ProductImage, Rating])