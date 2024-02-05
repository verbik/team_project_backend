from rest_framework import routers

from products.views import (
    ManufacturerViewSet,
    CountryViewSet,
    WineViewSet,
    GrapeVarietyViewSet,
)

router = routers.DefaultRouter()
router.register("manufacturers", ManufacturerViewSet, basename="manufacturers")
router.register("countries", CountryViewSet, basename="countries")
router.register("wines", WineViewSet, basename="wines")
router.register("grape-varieties", GrapeVarietyViewSet, basename="grape-variety")

urlpatterns = router.urls

app_name = "products"
