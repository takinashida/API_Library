
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, LoanViewSet
from library.apps import LibraryConfig


app_name=LibraryConfig.name

router = DefaultRouter()
router.register("author", AuthorViewSet)
router.register("book", BookViewSet)
router.register("loan", LoanViewSet)

urlpatterns=[
            ] + router.urls