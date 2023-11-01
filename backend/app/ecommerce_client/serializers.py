from rest_framework import serializers
from ecommerce_client import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'emoji', 'parent']

class CategoryWithChildrenSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()


    class Meta:
        model = models.Category
        fields = ['id', 'name', 'emoji', 'parent', 'children']
    
    def get_children(self, obj):
        c = models.Category.objects.filter(parent=obj.id)
        return CategorySerializer(c, many=True).data
    
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=models.Category.objects.all())
    class Meta:
        model = models.Product
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = "__all__"


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Click
        fields = "__all__"