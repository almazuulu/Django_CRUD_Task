from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Customer, Product

@receiver(post_save, sender=Customer)
def customer_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "notification_message",
                "message": f"New customer created: {instance.name}"
            }
        )

@receiver(post_save, sender=Product)
def product_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "notification_message",
                "message": f"New product added: {instance.name}"
            }
        )