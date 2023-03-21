from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from src.book.models import IMPORTANCE_LEVEL, BOOK_RATING, Author, Book
from django.core.validators import FileExtensionValidator
import os


class UserValidateSerializer(serializers.Serializer):
    user = serializers.IntegerField(min_value=1)

    @staticmethod
    def validate_user(user):
        try:
            User.objects.get(pk=user)
        except User.DoesNotExist:
            raise ValidationError('User not found!')
        return user


class AuthorValidateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, min_length=3)


class AuthorCreateSerializer(AuthorValidateSerializer):
    @staticmethod
    def validate_full_name(full_name):
        if Author.objects.filter(full_name=full_name).count() > 0:
            raise ValidationError('Author full name must be unique')
        return full_name


class AuthorUpdateSerializer(AuthorValidateSerializer):
    @staticmethod
    def validate_full_name(self, full_name):
        if Author.objects.filter(
                full_name=full_name).exclude(
            id=self.context.get('id')
        ).count() > 0:
            raise ValidationError('Author full name must be unique')
        return full_name


class BookValidateSerializer(UserValidateSerializer):
    title = serializers.CharField(max_length=255, min_length=2)
    author = serializers.ListField(
        min_length=1,
        child=serializers.IntegerField(min_value=1)
    )
    description = serializers.CharField(allow_null=True, allow_blank=True)
    file = serializers.FileField(
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf']
        )],
        allow_null=True
    )
    total_pages = serializers.IntegerField(min_value=1, max_value=10000)

    @staticmethod
    def validate_author(author):
        filtered_author = Author.objects.filter(id__in=author)
        if len(filtered_author) != len(author):
            raise ValidationError('Author not found')
        return author


class BookCreateSerializer(BookValidateSerializer):
    @staticmethod
    def validate_title(title):
        if Book.objects.filter(title=title).count() > 0:
            raise ValidationError('Title must be unique')
        return title


class BookUpdateSerializer(BookValidateSerializer):
    @staticmethod
    def validate_title(self, title):
        if Book.objects.filter(title=title).exclude(
                id=self.context.get('id')).count() > 0:
            raise ValidationError('Title must be unique')
        return title

    @staticmethod
    def validate_file(self, file):
        book = Book.objects.get(id=self.context.get('id'))
        try:
            file_path = book.file.path
        except ValueError:
            return file
        if book:
            file_exist = os.path.exists(file_path)
            if file_exist:
                file = os.path.basename(file_path)
                return file
            else:
                raise ValidationError(
                    'The file may have been deleted from '
                    'storage or moved to another location.'
                    ' Download the file again.'
                )
        return file


class UserBookValidateSerializer(UserValidateSerializer):
    book = serializers.IntegerField(min_value=1)
    importance = serializers.ChoiceField(
        choices=IMPORTANCE_LEVEL
    )
    pages_read = serializers.IntegerField(
        min_value=1, max_value=10000
    )


class UserBookCreateSerializer(UserBookValidateSerializer):
    @staticmethod
    def validate_pages_read(pages_read, book):
        book = Book.objects.get(pk=book)
        if pages_read > book.total_pages:
            raise ValidationError(
                'Количество прочитанных страниц не может быть '
                'больше общему количеству страниц в книге'
            )
        return pages_read

    @staticmethod
    def validate_book(book):
        try:
            Book.objects.get(pk=book)
        except Book.DoesNotExist:
            raise ValidationError('Book is not found')
        return book


class ReviewValidateSerializer(UserValidateSerializer):
    comment = serializers.CharField()
    rating = serializers.ChoiceField(
        choices=BOOK_RATING, allow_blank=False
    )
    book = serializers.IntegerField(min_value=1)

    @staticmethod
    def validate_book(book):
        try:
            Book.objects.get(pk=book)
        except Book.DoesNotExist:
            raise ValidationError('Book is not found')
        return book
