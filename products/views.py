from rest_framework import viewsets

from products.models import Manufacturer, Country, Wine, GrapeVariety
from products.serializers import (
    ManufacturerListSerializer,
    ManufacturerDetailSerializer,
    ManufacturerSerializer,
    CountrySerializer,
    WineSerializer,
    GrapeVarietySerializer,
    WineDetailSerializer,
    WineListSerializer,
)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class GrapeVarietyViewSet(viewsets.ModelViewSet):
    queryset = GrapeVariety.objects.all()
    serializer_class = GrapeVarietySerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ManufacturerListSerializer

        if self.action == "retrieve":
            return ManufacturerDetailSerializer

        return ManufacturerSerializer


class WineViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Wine.objects.all().select_related("manufacturer")

        if self.action == "retrieve":
            queryset = queryset.prefetch_related("grape_variety")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WineDetailSerializer

        if self.action == "list":
            return WineListSerializer

        return WineSerializer
