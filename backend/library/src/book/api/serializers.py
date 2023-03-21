from django.db.models import Sum, Avg
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from src.book.models import Author, Book, UserBook, Review


class AuthorSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id',
            'full_name'
        )


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = (
            'id',
            'user',
            'title',
            'author',
            'description',
            'file',
            'total_pages',
            'rating',
            'amount_reviews'
        )

    amount_reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    @staticmethod
    def get_amount_reviews(ob):
        return ob.review.all().aggregate(Sum('number'))['number__sum']

    @staticmethod
    def get_rating(ob):
        return ob.review.all().aggregate(Avg('rating'))['rating__avg']


class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields = (
            'id',
            'user',
            'book',
            'importance',
            'pages_read'
        )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'comment',
            'rating',
            'book',
            'creating_at'
        )
