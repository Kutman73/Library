from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Author(models.Model):
    """Book author model"""
    full_name = models.CharField(
        max_length=255, unique=True, null=False, blank=False
    )
    number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.full_name is not None:
            self.full_name = self.full_name.lower()
        if self.number != 1:
            self.number = 1
        super().save(*args, **kwargs)


IMPORTANCE_LEVEL = (
    (int(1), '1/3'),
    (int(2), '2/3'),
    (int(3), '3/3'),
)

BOOK_RATING = (
        (Decimal("1.0"), "★☆☆☆☆ (1/5)"),
        (Decimal("2.0"), "★★☆☆☆ (2/5)"),
        (Decimal("3.0"), "★★★☆☆ (3/5)"),
        (Decimal("4.0"), "★★★★☆ (4/5)"),
        (Decimal("5.0"), "★★★★★ (5/5)"),
)


class Book(models.Model):
    """Book model"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=255, unique=True)
    author = models.ManyToManyField(Author, related_name='book')
    description = models.TextField(
        blank=True, null=True
    )
    file = models.FileField(
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf']
        )],
        upload_to='books/',
        max_length=255
    )
    total_pages = models.PositiveIntegerField()
    number = models.PositiveSmallIntegerField(default=1)

    @property
    def average_rating(self):
        if hasattr(self, '_average_rating'):
            return self._average_rating
        return self.review.aggregate(models.Avg('rating'))

    @property
    def average_review(self):
        if hasattr(self, '_average_review'):
            return self._average_review
        return self.review.aggregate(models.Sum('number'))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.number != 1:
            self.number = 1
        super().save(*args, **kwargs)


class UserBook(models.Model):
    """User book model"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    importance = models.PositiveSmallIntegerField(choices=IMPORTANCE_LEVEL)
    pages_read = models.PositiveIntegerField(default=0)
    number = models.PositiveSmallIntegerField(default=1)

    def get_reading_progress(self):
        total_pages = self.book.total_pages
        if total_pages == 0:
            return 0
        else:
            return round(self.pages_read / total_pages * 100, 2)

    def __str__(self):
        return f"Книга '{self.book.title}' пользователя {self.user.username}"

    def save(self, *args, **kwargs):
        if self.pages_read > self.book.total_pages:
            self.pages_read = self.book.total_pages
        if self.number != 1:
            self.number = 1
        super().save(*args, **kwargs)
        self.book.save()


class Review(models.Model):
    """Review model"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.DecimalField(max_digits=2,
                                 decimal_places=1,
                                 choices=BOOK_RATING)
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             related_name='review')
    creating_at = models.DateField(auto_now_add=True)
    number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.user}_{self.book}_{self.comment[0:15]}"

    def save(self, *args, **kwargs):
        if self.number != 1:
            self.number = 1
        super().save(*args, **kwargs)
