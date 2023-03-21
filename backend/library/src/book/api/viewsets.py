from rest_framework.viewsets import ModelViewSet
from src.book.models import (
    Author,
    Book,
    UserBook,
    Review,
)
from src.book.api.serializers import (
    AuthorSerializer,
    BookSerializer,
    UserBookSerializer,
    ReviewSerializer,
)


class AuthorModelViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'pk'


class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'


class UserBookModelViewSet(ModelViewSet):
    queryset = UserBook.objects.all()
    serializer_class = UserBookSerializer
    lookup_field = 'pk'


class ReviewModelViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'pk'
