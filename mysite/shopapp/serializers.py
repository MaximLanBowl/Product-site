from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "description",
            "price",
            "discount",
            "create_at",
            "archive",
            "preview",

        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "pk",
            "user",
            "products",
            "delivery_adress",
            "created_at",
            "archive",
            "receipt",
            "promocode",
        )