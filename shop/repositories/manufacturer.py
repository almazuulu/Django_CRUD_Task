from django.db.models import QuerySet

from .base import BaseRepository
from ..models import Manufacturer


class ManufacturerRepository(BaseRepository[Manufacturer]):
    def __init__(self):
        super().__init__(Manufacturer)

    def get_by_country(self, country: str) -> QuerySet[Manufacturer]:
        return self.filter(country=country)
    
    def get_with_products(self) -> QuerySet[Manufacturer]:
        return self.get_all().select_related('product')
    
    def get_active_manufacturers(self) -> QuerySet[Manufacturer]:
        return self.filter(product__is_active=True).distinct()

    def get_by_contact_email(self, email: str) -> Manufacturer:
        return self.model_class.objects.get(contact_email=email)