from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from ecommerce_client.chroma_client import Chromaclient
from ecommerce_client.models import Product

# chroma_client = Chromaclient()

# class Command(BaseCommand):
#     help = "Utilities for the vector database"

#     def add_arguments(self, parser: CommandParser) -> None:
#         parser.add_argument("action", choices=["sync", "all", "is_synced"])

#     def handle(self, *args: Any, **options: Any) -> str | None:
        
#         action = options["action"]

#         if action == "sync":
        
#             self.stdout.write("Syncing SQL datbase with vector database ...")
#             all_embedded = chroma_client.get_all_ids()

#             all_products = Product.objects.all()

#             synced_count = 0
#             for product in all_products:
#                 if product.id not in all_embedded:
#                     chroma_client.add([product])
#                     synced_count += 1

#             self.stdout.write(f"Synced {synced_count} products with the database")

#         elif action == "all":
#             self.stdout.write(str(chroma_client.get_all_ids()))

