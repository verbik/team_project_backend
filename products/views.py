from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
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
    WineCreateSerializer,
    WineImageSerializer,
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

        if self.action in ["create", "update", "partial_update"]:
            return WineCreateSerializer

        if self.action == "upload_image":
            return WineImageSerializer

        return WineSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific wine instance."""
        wine = self.get_object()
        serializer = self.get_serializer(wine, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
