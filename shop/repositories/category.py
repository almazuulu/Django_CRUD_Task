from django.db.models.query import QuerySet

from .base import BaseRepository
from ..models import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    def get_with_products(self) -> QuerySet[Category]:
        return self.get_all().prefetch_related('products')