from django.shortcuts import render
from rest_framework import viewsets, generics, permissions

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializer


# Create your views here.
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]