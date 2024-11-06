from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Customer
from ..serializers import CustomerSerializer
from ..services.customer import CustomerService


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    service = CustomerService()

    def get_queryset(self):
        return self.service.get_all()

    def create(self, request, *args, **kwargs):
        """Create a new customer"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                customer = self.service.create(**serializer.validated_data)
                return Response(
                    {
                        "message": "Customer created successfully",
                        "data": self.get_serializer(customer).data
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
        """Update a customer"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            updated_customer = self.service.update(instance, **serializer.validated_data)
            return Response(
                {
                    "message": "Customer updated successfully",
                    "data": self.get_serializer(updated_customer).data
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a customer"""
        instance = self.get_object()
        self.service.delete(instance)
        return Response(
            {"message": "Customer deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        """Toggle product in favorites"""
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(
                {'error': 'Product ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = self.service.toggle_favorite_product(pk, product_id)
        if result['success']:
            return Response({"message": result['message']})
        return Response(
            {"error": result['message']},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active customers"""
        customers = self.service.get_active_customers()
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def favorites(self, request, pk=None):
        """Get customer's favorite products"""
        customer = self.get_object()
        favorites = self.service.get_customer_favorites(customer.id)
        from ..serializers import ProductSerializer
        serializer = ProductSerializer(favorites, many=True)
        return Response(serializer.data)