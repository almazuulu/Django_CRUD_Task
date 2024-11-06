from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import TemplateView

from .models import Category, Manufacturer, Product, Customer
from .serializers import (
    CategorySerializer, ManufacturerSerializer,
    ProductSerializer, CustomerSerializer
)


class WebSocketTestView(TemplateView):
    template_name = 'shop/websocket_test.html'

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products in category"""
        category = self.get_object()
        products = category.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'])
    def fans(self, request, pk=None):
        """Get all customers who favorited this product"""
        product = self.get_object()
        customers = product.favorited_by.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        """Toggle product in favorites"""
        customer = self.get_object()
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=400)
        
        try:
            product = Product.objects.get(id=product_id)
            if product in customer.favorite_products.all():
                customer.favorite_products.remove(product)
                action = 'removed from'
            else:
                customer.favorite_products.add(product)
                action = 'added to'
            return Response({
                'message': f'Product {action} favorites successfully'
            })
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
