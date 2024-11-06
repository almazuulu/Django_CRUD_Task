from django.db import models
from django.core.validators import EmailValidator
from .product import Product

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()]
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    favorite_products = models.ManyToManyField(
        Product, 
        related_name='favorited_by',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.email})"

    def get_favorite_products_count(self):
        return self.favorite_products.count()

    def add_to_favorites(self, product):
        self.favorite_products.add(product)

    def remove_from_favorites(self, product):
        self.favorite_products.remove(product)