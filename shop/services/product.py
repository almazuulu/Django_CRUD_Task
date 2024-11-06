from typing import List
from ..repositories.product import ProductRepository
from ..models import Product
from .base import BaseService


class ProductService(BaseService[Product]):
    def __init__(self):
        self.repository = ProductRepository()

    def get_products_by_category(self, category_id: int) -> List[Product]:
        return self.repository.get_by_category(category_id)

    def get_active_products(self) -> List[Product]:
        return self.repository.get_active_products()

    def update_stock(self, product_id: int, quantity: int) -> Product:
        product = self.get_by_id(product_id)
        if quantity >= 0:
            product = self.repository.update(product, stock=quantity)
        return product