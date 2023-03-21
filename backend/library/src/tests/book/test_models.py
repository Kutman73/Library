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
        self.assertEqual(self.author1.full_name, "test author1")
        self.assertEqual(self.author2.full_name, "test author2")

    def test_create_with_empty_name(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(full_name=None)

    def test_create_with_duplicate_name(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(full_name="Test Author1")

    def test_create_with_duplicate_name_case_insensitive(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(full_name="TeSt aUtHor1")

    def test_field_number(self):
        self.assertEqual(self.author1.number, 1)
        self.assertEqual(self.author2.number, 1)


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
        self.book2 = Book.objects.create(
            user=self.user,
            title="Test Book2",
            description="Test Description",
            file="test.pdf",
            total_pages=200
        )
        self.book.author.add(self.author)
        self.review1 = Review.objects.create(
            user=self.user,
            comment="Test Review 1",
            rating=4.0,
            book=self.book
        )
        self.review2 = Review.objects.create(
            user=self.user,
            comment="Test Review 2",
            rating=3.0,
            book=self.book
        )

    def test_book_user(self):
        self.assertEqual(self.book.user, self.user)
        self.assertEqual(self.book.user_id, self.user.id)

    def test_book_author(self):
        self.assertEqual(self.book.author.count(), 1)

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Book")
        self.assertEqual(self.book.title, "Test Book")

    def test_average_rating(self):
        self.assertEqual(self.book.average_rating['rating__avg'], 3.5)

    def test_average_review(self):
        self.assertEqual(self.book.average_review['number__sum'], 2)

    def test_field_number(self):
        self.assertEqual(self.book.number, 1)

    def test_save(self):
        self.book2.number = 9
        self.book2.save()
        self.assertEqual(self.book2.number, 1)


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
        self.assertEqual(
            str(self.user_book), "Книга 'Test Book' пользователя test user"
        )

    def test_get_reading_progress(self):
        self.assertEqual(self.user_book.get_reading_progress(), 50)

    def test_save(self):
        self.user_book.pages_read = 150
        self.user_book.save()
        self.assertEqual(self.user_book.pages_read, 100)

    def test_field_number(self):
        self.assertEqual(self.user_book.number, 1)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test user', password='12345'
        )
        self.author = Author.objects.create(full_name="Test Author")
        self.book = Book.objects.create(
            user=self.user,
            title="Test Book",
            description="Test Description",
            file="test.pdf",
            total_pages=100
        )
        self.book.author.add(self.author)
        self.review = Review.objects.create(
            user=self.user,
            comment="Test Review",
            rating=4.0,
            book=self.book
        )

    def test_validate_book(self):
        self.assertEqual(self.review.book, self.book)
        self.assertEqual(self.review.book_id, self.book.id)

    def test_review_str(self):
        self.assertEqual(str(self.review), "test user_Test Book_Test Review")

    def test_field_number(self):
        self.assertEqual(self.review.number, 1)
