from typing import List, Optional
from ..repositories.manufacturer import ManufacturerRepository
from ..models import Manufacturer
from .base import BaseService


class ManufacturerService(BaseService[Manufacturer]):
    def __init__(self):
        self.repository = ManufacturerRepository()

    def get_manufacturers_by_country(self, country: str) -> List[Manufacturer]:
        """Get all manufacturers from a specific country"""
        return self.repository.get_by_country(country)

    def get_manufacturers_with_products(self) -> List[Manufacturer]:
        """Get all manufacturers with their related products"""
        return self.repository.get_with_products()

    def get_active_manufacturers(self) -> List[Manufacturer]:
        """Get manufacturers that have active products"""
        return self.repository.get_active_manufacturers()

    def create_manufacturer(self, data: dict) -> Manufacturer:
        """Create a new manufacturer with validation"""
        # additoianl lgoic before creating
        if self.repository.filter(contact_email=data.get('contact_email')).exists():
            raise ValueError("Manufacturer with this email already exists")
        
        return self.repository.create(**data)

    def update_contacts(self, 
                       manufacturer_id: int, 
                       email: Optional[str] = None, 
                       phone: Optional[str] = None, 
                       website: Optional[str] = None) -> Manufacturer:
        """Update manufacturer contact information"""
        manufacturer = self.get_by_id(manufacturer_id)
        update_data = {}
        
        if email:
            update_data['contact_email'] = email
        if phone:
            update_data['contact_phone'] = phone
        if website:
            update_data['website'] = website
            
        return self.repository.update(manufacturer, **update_data)

    def get_by_email(self, email: str) -> Optional[Manufacturer]:
        """Get manufacturer by contact email"""
        try:
            return self.repository.get_by_contact_email(email)
        except Manufacturer.DoesNotExist:
            return None