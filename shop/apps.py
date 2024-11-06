from django.apps import AppConfig

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'Shop Management'

    def ready(self):
        try:
            import shop.signals
        except ImportError:
            pass