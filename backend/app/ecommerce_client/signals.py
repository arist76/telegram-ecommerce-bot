from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ecommerce_client.models import Product
from ecommerce_client.chroma_client import Chromaclient

# chroma_client = Chromaclient()

# @receiver(post_save, sender=Product)
# def product_save_signal(sender, instance : Product, created : bool, **kwargs):
#     chroma_client.upsert([instance])
#     print(f"product id {instance.id} embedded to chroma")


# @receiver(post_delete, sender=Product)
# def product_delete_signal(sender, instance : Product, **kwargs):
#     chroma_client.delete([instance])
#     print(f"product id {instance.id} deleted from chroma")
