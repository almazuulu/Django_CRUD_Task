from django.db import models

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Category name must be unique"
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_products_count(self):
        return self.product_set.count()