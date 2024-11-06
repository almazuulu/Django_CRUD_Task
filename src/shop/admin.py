from django.contrib import admin
from .models import Category, Manufacturer, Product, Customer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'website', 'created_at')
    search_fields = ('name', 'country')
    list_filter = ('country', 'created_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'manufacturer', 'is_active')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('name', 'description')
    raw_id_fields = ('category', 'manufacturer')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email')
    filter_horizontal = ('favorite_products',)
