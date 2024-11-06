from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Customer, Product, Category, Manufacturer
from .serializers import (
    CustomerSerializer, 
    ProductSerializer, 
    CategorySerializer,
    ManufacturerSerializer
)

# Customer signals
@receiver(post_save, sender=Customer)
def customer_saved(sender, instance, created, **kwargs):
    """Signal for customer creation or update"""
    channel_layer = get_channel_layer()
    serializer = CustomerSerializer(instance)
    
    async_to_sync(channel_layer.group_send)(
        "shop_updates",
        {
            "type": "notify_customer_update",
            "customer": serializer.data,
            "action": "created" if created else "updated",
            "message": f"New customer {'created' if created else 'updated'}: {instance.name}"
        }
    )

@receiver(post_delete, sender=Customer)
def customer_deleted(sender, instance, **kwargs):
    """Signal for customer deletion"""
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        "shop_updates",
        {
            "type": "notify_customer_update",
            "customer": {
                "id": instance.id,
                "name": instance.name,
                "email": instance.email
            },
            "action": "deleted",
            "message": f"Customer deleted: {instance.name}"
        }
    )

# Product signals
@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    """Signal for product creation or update"""
    channel_layer = get_channel_layer()
    serializer = ProductSerializer(instance)
    
    async_to_sync(channel_layer.group_send)(
        "shop_updates",
        {
            "type": "notify_product_update",
            "product": serializer.data,
            "action": "created" if created else "updated",
            "message": f"New product {'created' if created else 'updated'}: {instance.name}"
        }
    )

@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    """Signal for product deletion"""
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        "shop_updates",
        {
            "type": "notify_product_update",
            "product": {
                "id": instance.id,
                "name": instance.name,
                "sku": instance.sku
            },
            "action": "deleted",
            "message": f"Product deleted: {instance.name}"
        }
    )

# Category signals
@receiver(post_save, sender=Category)
def category_saved(sender, instance, created, **kwargs):
    """Signal for category creation or update"""
    channel_layer = get_channel_layer()
    serializer = CategorySerializer(instance)
    
    async_to_sync(channel_layer.group_send)(
        "shop_updates",
        {
            "type": "notify_category_update",
            "category": serializer.data,
            "action": "created" if created else "updated",
            "message": f"Category {'created' if created else 'updated'}: {instance.name}"
        }
    )

@receiver(post_delete, sender=Category)
def category_deleted(sender, instance, **kwargs):
    """Signal for category deletion"""
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        "shop_updates",
        {
            "type": "notify_category_update",
            "category": {
                "id": instance.id,
                "name": instance.name
            },
            "action": "deleted",
            "message": f"Category deleted: {instance.name}"
        }
    )

# Manufacturer signals
@receiver(post_save, sender=Manufacturer)
def manufacturer_saved(sender, instance, created, **kwargs):
    """Signal for manufacturer creation or update"""
    channel_layer = get_channel_layer()
    serializer = ManufacturerSerializer(instance)
    
    async_to_sync(channel_layer.group_send)(
        "shop_updates",
        {
            "type": "notify_manufacturer_update",
            "manufacturer": serializer.data,
            "action": "created" if created else "updated",
            "message": f"Manufacturer {'created' if created else 'updated'}: {instance.name}"
        }
    )

@receiver(post_delete, sender=Manufacturer)
def manufacturer_deleted(sender, instance, **kwargs):
    """Signal for manufacturer deletion"""
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        "shop_updates",
        {
            "type": "notify_manufacturer_update",
            "manufacturer": {
                "id": instance.id,
                "name": instance.name,
                "country": instance.country
            },
            "action": "deleted",
            "message": f"Manufacturer deleted: {instance.name}"
        }
    )