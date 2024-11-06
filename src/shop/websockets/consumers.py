import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from ..models import Product, Category, Customer, Manufacturer

class ShopConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Establish connection and add to group"""
        self.group_name = 'shop_updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to shop websocket'
        }))

    async def disconnect(self, close_code):
        """Disconnect from group"""
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle incoming messages"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', '')
           
            if message_type == 'subscribe_to_product':
                product_id = text_data_json.get('product_id')
                await self.subscribe_to_product(product_id)
            elif message_type == 'subscribe_to_category':
                category_id = text_data_json.get('category_id')
                await self.subscribe_to_category(category_id)
            elif message_type == 'subscribe_to_customer':
                customer_id = text_data_json.get('customer_id')
                await self.subscribe_to_customer(customer_id)
            elif message_type == 'subscribe_to_manufacturer':
                manufacturer_id = text_data_json.get('manufacturer_id')
                await self.subscribe_to_manufacturer(manufacturer_id)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))

    async def notify_product_update(self, event):
        """Send product update notification"""
        await self.send(text_data=json.dumps({
            'type': 'product_update',
            'product': event['product'],
            'action': event.get('action', 'updated')
        }))

    async def notify_category_update(self, event):
        """Send category update notification"""
        await self.send(text_data=json.dumps({
            'type': 'category_update',
            'category': event['category'],
            'action': event.get('action', 'updated')
        }))

    async def notify_customer_update(self, event):
        """Send customer update notification"""
        await self.send(text_data=json.dumps({
            'type': 'customer_update',
            'customer': event['customer'],
            'action': event.get('action', 'updated')
        }))

    async def notify_manufacturer_update(self, event):
        """Send manufacturer update notification"""
        await self.send(text_data=json.dumps({
            'type': 'manufacturer_update',
            'manufacturer': event['manufacturer'],
            'action': event.get('action', 'updated')
        }))

    @database_sync_to_async
    def subscribe_to_product(self, product_id):
        """Subscribe to updates for a specific product"""
        try:
            product = Product.objects.get(id=product_id)
            return {'id': product.id, 'name': product.name}
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def subscribe_to_category(self, category_id):
        """Subscribe to updates for a specific category"""
        try:
            category = Category.objects.get(id=category_id)
            return {'id': category.id, 'name': category.name}
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def subscribe_to_customer(self, customer_id):
        """Subscribe to updates for a specific customer"""
        try:
            customer = Customer.objects.get(id=customer_id)
            return {'id': customer.id, 'name': customer.name}
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def subscribe_to_manufacturer(self, manufacturer_id):
        """Subscribe to updates for a specific manufacturer"""
        try:
            manufacturer = Manufacturer.objects.get(id=manufacturer_id)
            return {'id': manufacturer.id, 'name': manufacturer.name}
        except ObjectDoesNotExist:
            return None