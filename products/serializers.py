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

    class Meta:
        model = Wine
        fields = BeverageSerializer.Meta.fields + (
            "year",
            "sugar_content",
            "color",
            "grape_variety",
            "image",
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


class WineListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wine
        fields = ("id", "image", "short_description", "price", "product_code")


class WineImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = ("id", "image")
