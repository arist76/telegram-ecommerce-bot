from django.db.models import Count
from rest_framework import serializers
from ecommerce_client import models


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ["uuid", "name", "parent", "product_count"]

    def get_product_count(self, obj):
        return models.Product.objects.filter(category=obj).count()


class CategoryWithChildrenSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ["uuid", "name", "parent", "children"]

    def get_children(self, obj):
        if self.context.get("with_product"):
            children = models.Category.objects.get_only_product_queryset().filter(
                parent=obj.uuid
            )
        else:
            children = models.Category.objects.filter(parent=obj.uuid)

        return CategorySerializer(children, many=True).data


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ["uuid", "image", "product"]
        read_only_fields = ["uuid"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = models.Product
        fields = "__all__"
        read_only_fields = ["sold", "posted", "last_modified"]

    def create(self, validated_data):
        images_data = validated_data.pop("images")
        product = models.Product.objects.create(**validated_data)
        for image_data in images_data:
            models.ProductImage.objects.create(product=product, **image_data)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images")
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.save()

        # Handle images
        for image_data in images_data:
            image_id = image_data.get("uuid")
            if image_id:
                image_instance = models.ProductImage.objects.get(
                    uuid=image_id, product=instance
                )
                image_instance.image = image_data.get("image", image_instance.image)
                image_instance.save()
            else:
                models.ProductImage.objects.create(product=instance, **image_data)

        return instance


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = "__all__"


class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Saved
        fields = "__all__"


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Click
        fields = "__all__"
