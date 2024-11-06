from django.db.models.query import QuerySet

from .base import BaseRepository
from ..models import Customer


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self):
        super().__init__(Customer)

    def get_active_customers(self) -> QuerySet[Customer]:
        return self.filter(is_active=True)

    def get_with_favorites(self) -> QuerySet[Customer]:
        return self.get_all().prefetch_related('favorite_products')