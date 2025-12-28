from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserUpdateAPIView, UserListAPIView

app_name=UsersConfig.name

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),

    path("registration/", UserCreateAPIView.as_view(), name="user_create"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path("", UserListAPIView.as_view(), name="user_list"),
]