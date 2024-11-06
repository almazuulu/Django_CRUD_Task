from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from .category import Category
from .manufacturer import Manufacturer

class Product(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Product name must be unique"
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='products'
    )
    manufacturer = models.OneToOneField(
        Manufacturer, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='product'
    )
    sku = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['sku']),
        ]

    def __str__(self):
        return self.name

    def get_price_with_tax(self, tax_rate=0.20):
        return self.price * (1 + tax_rate)

    def is_in_stock(self):
        return self.stock > 0