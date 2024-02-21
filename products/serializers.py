from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from comments.serializers import CommentSerializer
from products.models import Manufacturer, Country, Beverage, Wine, GrapeVariety


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class GrapeVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = GrapeVariety
        fields = (
            "id",
            "name",
        )


class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = (
            "id",
            "name",
            "info",
            "country_of_origin",
            "website",
        )


class ManufacturerListSerializer(serializers.ModelSerializer):
    country_of_origin = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Manufacturer
        fields = ("id", "name", "country_of_origin")


class ManufacturerDetailSerializer(ManufacturerSerializer):
    country_of_origin = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )


class BeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beverage
        fields = (
            "id",
            "name",
            "price",
            "description",
            "manufacturer",
            "product_code",
            "country",
            "region",
            "alcohol_content",
            "volume",
            "image",
        )
        read_only_fields = ("image",)


class WineSerializer(BeverageSerializer):
    class Meta:
        model = Wine
        fields = BeverageSerializer.Meta.fields + (
            "year",
            "sugar_content",
            "color",
            "grape_variety",
        )
        read_only_fields = ("image",)

    #  TODO: add nested serializer


class WineCreateSerializer(serializers.ModelSerializer):
    grape_variety = GrapeVarietySerializer(read_only=False, many=True)

    def validate(self, attrs):
        data = super(WineCreateSerializer, self).validate(attrs=attrs)
        Beverage.validate_region(attrs["region"], attrs["country"], ValidationError)
        Beverage.validate_product_code(attrs["product_code"], ValidationError)
        return data

    class Meta:
        model = Wine
        fields = (
            "id",
            "name",
            "price",
            "description",
            "product_code",
            "alcohol_content",
            "volume",
            "year",
            "sugar_content",
            "color",
            "manufacturer",
            "country",
            "region",
            "grape_variety",
        )

    def create(self, validated_data):
        grape_variety_data = validated_data.pop("grape_variety", [])
        wine = Wine.objects.create(**validated_data)
        for variety_data in grape_variety_data:
            variety, _ = GrapeVariety.objects.get_or_create(**variety_data)
            wine.grape_variety.add(variety)
        return wine

    def update(self, instance, validated_data):
        grape_variety_data = validated_data.pop("grape_variety", [])
        instance = super().update(instance, validated_data)

        # Clear existing grape_variety and add new ones
        instance.grape_variety.clear()
        for variety_data in grape_variety_data:
            variety, _ = GrapeVariety.objects.get_or_create(**variety_data)
            instance.grape_variety.add(variety)

        return instance


class WineDetailSerializer(WineSerializer):
    grape_variety = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    country = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    manufacturer = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Wine
        fields = WineSerializer.Meta.fields + ("comments",)


class WineListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wine
        fields = ("id", "image", "short_description", "price", "product_code")


class WineImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = ("id", "image")
