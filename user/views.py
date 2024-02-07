from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets

from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserChangePasswordSerializer,
)


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response(status=status.HTTP_201_CREATED)
        return response


class UserDetailViewSet(viewsets.ModelViewSet):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.request.user.pk)

    def get_serializer_class(self):
        if self.action == "change_password":
            return UserChangePasswordSerializer
        else:
            return UserDetailSerializer

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    @action(methods=["POST"], detail=True, url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user, data=request.data)

        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response(
                {"success": "Password changed successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
