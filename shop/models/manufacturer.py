from django.db import models
from django.core.validators import URLValidator

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    website = models.URLField(
        blank=True,
        validators=[URLValidator(schemes=['http', 'https'])]
    )
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_full_contact(self):
        return f"{self.name} ({self.country})"