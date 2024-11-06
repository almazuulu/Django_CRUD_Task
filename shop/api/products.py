from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Product
from ..utils import ReadOnlyOrAuthenticated
from ..serializers import ProductSerializer, CustomerSerializer
from ..services.product import ProductService


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    service = ProductService()
    permission_classes = [ReadOnlyOrAuthenticated]
    
    def get_queryset(self):
        return self.service.get_all()

    def create(self, request, *args, **kwargs):
        """Create a new product"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                product = self.service.create(**serializer.validated_data)
                return Response(
                    {
                        "message": "Product created successfully",
                        "data": self.get_serializer(product).data
                    },
                    status=status.HTTP_201_CREATED
                )
            except ValueError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Update a product"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            updated_product = self.service.update(instance, **serializer.validated_data)
            return Response(
                {
                    "message": "Product updated successfully",
                    "data": self.get_serializer(updated_product).data
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a product"""
        instance = self.get_object()
        self.service.delete(instance)
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['get'])
    def fans(self, request, pk=None):
        """Get customers who favorited this product"""
        product = self.get_object()
        fans = self.service.get_product_fans(product.id)
        serializer = CustomerSerializer(fans, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_stock(self, request, pk=None):
        """Update product stock"""
        quantity = request.data.get('quantity')
        if quantity is None:
            return Response(
                {'error': 'Quantity is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = self.service.update_stock(pk, quantity)
            return Response({
                "message": "Stock updated successfully",
                "data": self.get_serializer(product).data
            })
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def in_stock(self, request):
        """Get all products in stock"""
        products = self.service.get_active_products()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)