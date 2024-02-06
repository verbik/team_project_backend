from rest_framework import serializers

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


#  TODO: add nested serializer
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


class WineSerializer(BeverageSerializer):
    class Meta:
        model = Wine
        fields = BeverageSerializer.Meta.fields + (
            "year",
            "sugar_content",
            "color",
            "grape_variety",
        )

    #  TODO: add nested serializer


class WineDetailSerializer(WineSerializer):
    grape_variety = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    country = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )


class WineListSerializer(WineSerializer):
    pass
