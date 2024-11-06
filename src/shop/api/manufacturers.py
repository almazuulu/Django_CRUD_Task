from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Manufacturer
from ..utils import ReadOnlyOrAuthenticated
from ..serializers import ManufacturerSerializer
from ..services.manufacturer import ManufacturerService


class ManufacturerViewSet(viewsets.ModelViewSet):
    serializer_class = ManufacturerSerializer
    service = ManufacturerService()
    permission_classes = [ReadOnlyOrAuthenticated]

    def get_queryset(self):
        return self.service.get_all()

    def create(self, request, *args, **kwargs):
        """Create a new manufacturer"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                manufacturer = self.service.create_manufacturer(serializer.validated_data)
                return Response(
                    {
                        "message": "Manufacturer created successfully",
                        "data": self.get_serializer(manufacturer).data
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
        """Update a manufacturer"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            updated_instance = self.service.update(instance, **serializer.validated_data)
            return Response(
                {
                    "message": "Manufacturer updated successfully",
                    "data": self.get_serializer(updated_instance).data
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a manufacturer"""
        instance = self.get_object()
        self.service.delete(instance)
        return Response(
            {"message": "Manufacturer deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    def by_country(self, request):
        """Get manufacturers by country"""
        country = request.query_params.get('country')
        if not country:
            return Response(
                {"error": "Country parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        manufacturers = self.service.get_manufacturers_by_country(country)
        serializer = self.get_serializer(manufacturers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get manufacturers with active products"""
        manufacturers = self.service.get_active_manufacturers()
        serializer = self.get_serializer(manufacturers, many=True)
        return Response(serializer.data)

    def update_contacts(self, request, pk=None):
        """Update manufacturer contact information"""
        email = request.data.get('email')
        phone = request.data.get('phone')
        website = request.data.get('website')

        try:
            manufacturer = self.service.update_contacts(
                manufacturer_id=pk,
                email=email,
                phone=phone,
                website=website
            )
            return Response({
                "message": "Contact information updated successfully",
                "data": self.get_serializer(manufacturer).data
            })
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )