from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsOwner
from .models import Author
from .serializers import AuthorSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Loan
from .serializers import LoanSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
import json

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAuthenticated,)

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("author", "genre")
    search_fields = ("title",)
    permission_classes = (IsAuthenticated,)

class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.select_related("user", "book")
    serializer_class = LoanSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

    def perform_create(self, serializer, send_loan_reminder=None):
        loan = serializer.save(user=self.request.user)

        notify_at = loan.return_at - timedelta(days=2)

        if notify_at > timezone.now():
            send_loan_reminder.apply_async(
                args=[loan.id],
                eta=notify_at
            )

    def perform_destroy(self, serializer):
        loan = serializer.save(user=self.request.user)


