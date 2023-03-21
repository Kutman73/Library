from django.urls import path, include
from rest_framework import routers
from src.book.api.viewsets import (
    AuthorModelViewSet,
    BookModelViewSet,
    UserBookModelViewSet,
    ReviewModelViewSet
)

router = routers.DefaultRouter()
router.register(r'authors', AuthorModelViewSet)
router.register(r'books', BookModelViewSet)
router.register(r'user-books', UserBookModelViewSet)
router.register(r'reviews', ReviewModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]
