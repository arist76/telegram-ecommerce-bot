from django.apps import AppConfig


class EcommerceClientConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ecommerce_client"

    def ready(self) -> None:
        from ecommerce_client import signals
