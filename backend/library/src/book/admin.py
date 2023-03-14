from django.contrib import admin
from src.book.models import Author, Book, UserBook, Review

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(UserBook)
admin.site.register(Review)
