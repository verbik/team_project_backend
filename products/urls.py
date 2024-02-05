from rest_framework import routers

from products.views import ManufacturerViewSet, CountryViewSet

router = routers.DefaultRouter()
router.register("manufacturers", ManufacturerViewSet, basename="manufacturers")
router.register("countries", CountryViewSet, basename="countries")

urlpatterns = router.urls

app_name = "products"
