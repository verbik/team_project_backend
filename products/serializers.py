from rest_framework import serializers

from products.models import Manufacturer, Country, Beverage, Wine


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


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
        )


class WineSerializer(BeverageSerializer):
    class Meta:
        model = Wine
        fields = BeverageSerializer.Meta.fields + (
            "year",
            "sugar_content",
            "color",
            "grape_variety",
        )
