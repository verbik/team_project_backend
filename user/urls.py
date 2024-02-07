from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import UserDetailViewSet, RegisterView

router = DefaultRouter()
router.register("me", UserDetailViewSet, basename="user-detail")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register_user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls

app_name = "user"
