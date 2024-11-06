from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Category
from ..utils import ReadOnlyOrAuthenticated
from ..serializers import CategorySerializer, ProductSerializer
from ..services.category import CategoryService


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    service = CategoryService()
    permission_classes = [ReadOnlyOrAuthenticated]

    def get_queryset(self):
        return self.service.get_all()

    def create(self, request, *args, **kwargs):
        """Create a new category"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                category = self.service.create(**serializer.validated_data)
                return Response(
                    {
                        "message": "Category created successfully",
                        "data": self.get_serializer(category).data
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
        """Update a category"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            updated_category = self.service.update(instance, **serializer.validated_data)
            return Response(
                {
                    "message": "Category updated successfully",
                    "data": self.get_serializer(updated_category).data
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a category"""
        instance = self.get_object()
        self.service.delete(instance)
        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products in category"""
        products = self.service.get_category_products(pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def with_products(self, request):
        """Get all categories with their products"""
        categories = self.service.get_categories_with_products()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
