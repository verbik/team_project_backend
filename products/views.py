from rest_framework import viewsets

from products.models import Manufacturer, Country
from products.serializers import (
    ManufacturerListSerializer,
    ManufacturerDetailSerializer,
    ManufacturerSerializer,
    CountrySerializer,
)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ManufacturerListSerializer

        if self.action == "retrieve":
            return ManufacturerDetailSerializer

        return ManufacturerSerializer
