from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from src.book.models import (
    Author,
    Book,
    UserBook,
    Review,
)


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(full_name="Test Author1")
        self.author2 = Author.objects.create(full_name="Test Author2")

    def test_create_with_valid_name(self):
        author3 = Author.objects.create(full_name="Test Author3")
        self.assertEqual(author3.full_name, "test author3")

    def test_create_with_empty_name(self):
        with self.assertRaises(IntegrityError):
            # if you pass an empty string,
            # then it will be saved in the database as an empty string
            Author.objects.create(full_name=None)

    def test_create_with_duplicate_name(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(full_name="Test Author1")

    def test_create_with_duplicate_name_case_insensitive(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(full_name="TeSt aUtHor1")


class BookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test user', password='12345')
        self.author = Author.objects.create(full_name="Test Author")
        self.book = Book.objects.create(
            user=self.user,
            title="Test Book",
            description="Test Description",
            file="test.pdf",
            total_pages=100
        )
        self.book.author.add(self.author)

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Book")

    def test_average_rating(self):
        Review.objects.create(
            author=self.user,
            comment="Test Review 1",
            rating=4.0,
            book=self.book
        )
        Review.objects.create(
            author=self.user,
            comment="Test Review 2",
            rating=3.0,
            book=self.book
        )
        self.assertEqual(self.book.average_rating['rating__avg'], 3.5)


class UserBookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test user', password='12345')
        self.author = Author.objects.create(full_name="Test Author")
        self.book = Book.objects.create(
            user=self.user,
            title="Test Book",
            description="Test Description",
            file="test.pdf",
            total_pages=100
        )
        self.book.author.add(self.author)
        self.user_book = UserBook.objects.create(
            user=self.user,
            book=self.book,
            importance=1,
            pages_read=50
        )

    def test_user_book_str(self):
        self.assertEqual(str(self.user_book), "Книга 'Test Book' пользователя test user")

    def test_get_reading_progress(self):
        self.assertEqual(self.user_book.get_reading_progress(), 50)

    def test_save(self):
        self.user_book.pages_read = 150
        self.user_book.save()
        self.assertEqual(self.user_book.pages_read, 100)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test user', password='12345')
        self.author = Author.objects.create(full_name="Test Author")
        self.book = Book.objects.create(
            user=self.user,
            title="Test Book",
            description="Test Description",
            file="test.pdf",
            total_pages=100
        )
        self.book.author.add(self.author)

    def test_review_str(self):
        review = Review.objects.create(
            author=self.user,
            comment="Test Review",
            rating=4.0,
            book=self.book
        )
        self.assertEqual(str(review), "Test Review")
