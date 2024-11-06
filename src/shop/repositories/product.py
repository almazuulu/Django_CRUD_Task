from django.db.models.query import QuerySet

from .base import BaseRepository
from ..models import Product


class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)

    def get_by_category(self, category_id: int) -> QuerySet[Product]:
        return self.filter(category_id=category_id)

    def get_active_products(self) -> QuerySet[Product]:
        return self.filter(is_active=True)

    def get_in_stock(self) -> QuerySet[Product]:
        return self.filter(stock__gt=0)