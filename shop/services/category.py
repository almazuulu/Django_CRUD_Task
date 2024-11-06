from ..repositories.category import CategoryRepository
from ..models import Category
from .base import BaseService


class CategoryService(BaseService[Category]):
    def __init__(self):
        self.repository = CategoryRepository()

    def get_categories_with_products(self):
        return self.repository.get_with_products()