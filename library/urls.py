from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, LoanViewSet
from library.apps import LibraryConfig


app_name=LibraryConfig.name

router = DefaultRouter()
router.register("author", AuthorViewSet)
router.register("book", BookViewSet)
router.register("loan", LoanViewSet)

urlpatterns=[
            path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
            path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="library:schema")),
            ] + router.urls