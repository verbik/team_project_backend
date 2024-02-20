from rest_framework import viewsets, status
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import (
    OrderSerializer,
    OrderListSerializer,
    OrderAdminListSerializer,
    OrderDetailSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        request_user = self.request.user

        if not request_user.is_staff:
            queryset = queryset.filter(user_id=request_user.id)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            if self.request.user.is_staff:
                return OrderAdminListSerializer
            return OrderListSerializer

        if self.action == "retrieve":
            return OrderDetailSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)

        # Proceed with creating the new order
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
