from rest_framework import routers

from orders.views import OrderViewSet

orders_router = routers.DefaultRouter()
orders_router.register("orders", OrderViewSet, basename="orders")

app_name = "orders"
