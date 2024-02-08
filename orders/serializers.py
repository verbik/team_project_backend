from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import transaction
from rest_framework import serializers

from orders.models import OrderItem, Order


class ContentTypeField(serializers.Field):
    """A custom field to use for 'content_object' generic relationship."""

    def to_internal_value(self, data):
        try:
            model_name = data.lower()
            return ContentType.objects.get(model=model_name)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError(f"Invalid content type: {data}")

    def to_representation(self, value):
        return value.model


class OrderItemSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField()
    object_id = serializers.IntegerField()
    quantity = serializers.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "content_type",
            "object_id",
            "quantity",
            "item_price",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "user", "is_paid", "total_price", "items")
        read_only_fields = ("total_price", "user")

    def create(self, validated_data):
        with transaction.atomic():
            items_data = validated_data.pop("items")
            order = Order.objects.create(**validated_data)
            for item_data in items_data:

                OrderItem.objects.create(order=order, **item_data)
            return order


class OrderListSerializer(OrderSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
