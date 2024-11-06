from ..repositories.customer import CustomerRepository
from ..models import Customer, Product
from .base import BaseService


class CustomerService(BaseService[Customer]):
    def __init__(self):
        self.repository = CustomerRepository()

    def toggle_favorite_product(self, customer_id: int, product_id: int) -> dict:
        customer = self.get_by_id(customer_id)
        try:
            product = Product.objects.get(id=product_id)
            if product in customer.favorite_products.all():
                customer.favorite_products.remove(product)
                action = 'removed from'
            else:
                customer.favorite_products.add(product)
                action = 'added to'
            return {
                'success': True,
                'message': f'Product {action} favorites successfully'
            }
        except Product.DoesNotExist:
            return {
                'success': False,
                'message': 'Product not found'
            }