from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
from ecommerce_client.models import *
from app.settings import BASE_DIR
import os
import tempfile
import git
import logging
import json
import yaml
import uuid

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load categories from git repo"

    # def add_arguments(self, parser: BaseCommand) -> None:
    #     # set optional argument
    #     parser.add_argument("repo", type=str)

    def handle(self, *args, **options) -> str | None:

        # repo = options["repo"]

        # if not repo:
        #     repo = "git@github.com:Shopify/product-taxonomy.git"

        repo = "https://github.com/arist76/spotify-product-taxonomy.git"
        git.Git().execute(
            ["git", "config", "--global", "http.postBuffer", "1048576000"]
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # tmpdir = "./tmpdir"

            # check tmpdir exisists
            os.makedirs(tmpdir, exist_ok=True)
            print(f"Cloning {repo} to {tmpdir}")
            git.Repo.clone_from(repo, tmpdir)
            print(f"Cloned {repo} to {tmpdir}")

            value_file_dir = os.path.join(tmpdir, "data", "values.yml")
            attribute_file_dir = os.path.join(tmpdir, "data", "attributes.yml")
            category_folder_dir = os.path.join(tmpdir, "data", "categories")
            # get all files in the directory
            category_files_dir = os.listdir(category_folder_dir)

            # create values
            with open(value_file_dir, "r") as f:
                values = yaml.safe_load(f)
                create_values(values)

            # create attributes
            with open(attribute_file_dir, "r") as f:
                attributes = yaml.safe_load(f)
                base_attributes = attributes["base_attributes"]
                extended_attributes = attributes["extended_attributes"]

                create_attributes(base_attributes)
                create_extended_attributes(extended_attributes)

            for cat_files in category_files_dir:
                print(f"Loading {cat_files}")
                with open(os.path.join(category_folder_dir, cat_files), "r") as f:
                    categories = yaml.safe_load(f)
                    create_categories(categories)


def create_values(values):
    print(" > Creating values")
    for value in values:
        print(f"    > Creating value {value['name']}")
        ValueOption.objects.create(
            schema_id=value["id"],
            name=value["name"],
            schema_friendly_id=value["friendly_id"],
            handle=value["handle"],
        )


def create_attributes(attributes):
    print(" > Creating attributes")
    values = []
    for attribute in attributes:
        print(f"    > Creating attribute {attribute['name']}")
        values = attribute.pop("values")
        attribute = Attribute.objects.create(
            schema_id=attribute["id"],
            name=attribute["name"],
            description=attribute["description"],
            friendly_id=attribute["friendly_id"],
            handle=attribute["handle"],
        )
        create_values_to_attributes(attribute, values)


def create_extended_attributes(extended_attributes):
    print(f" > Creating extended attributes")
    for attribute in extended_attributes:
        print(f"    > Creating extended attribute {attribute['name']}")
        values_from_attr = Attribute.objects.get(friendly_id=attribute["values_from"])
        values_from_attr = AttributeValueOptions.objects.filter(
            attribute=values_from_attr
        )
        values_from_attr = values_from_attr.values_list(
            "value__schema_friendly_id", flat=True
        )
        attribute = Attribute.objects.create(
            name=attribute["name"],
            description=attribute["description"],
            friendly_id=attribute["friendly_id"],
            handle=attribute["handle"],
        )

        create_values_to_attributes(attribute, values_from_attr)


def create_values_to_attributes(attribute, values):
    print(f" > Creating values for attribute {attribute.name}")
    for value in values:
        print(f"    > Creating value {value} for attribute {attribute.name}")
        attr_val = ValueOption.objects.get(schema_friendly_id=value)
        AttributeValueOptions.objects.create(attribute=attribute, value=attr_val)


def create_categories(categories):
    print(f" > Creating categories")
    for category in categories:
        print(f"    > Creating category {category['name']}")
        parent = (
            None
            if len(category["id"].split("-")) == 1
            else Category.objects.get(
                schema_id="-".join(category["id"].split("-")[:-1])
            )
        )
        attributes = category.pop("attributes")
        category = Category.objects.create(
            schema_id=category["id"], name=category["name"], parent=parent
        )

        create_category_attribute(category, attributes)


def create_category_attribute(category, attributes):
    print(f" > Creating attributes for category {category.name}")
    for attribute in attributes:
        print(f"    > Creating attribute {attribute} for category {category.name}")
        CategoryAttribute.objects.create(
            category=category,
            attribute=Attribute.objects.get(friendly_id=attribute),
        )
