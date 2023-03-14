from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


class Author(models.Model):
    """Book author model"""
    full_name = models.CharField(max_length=255, unique=True, null=False, blank=False)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.full_name is not None:
            self.full_name = self.full_name.lower()
        super().save(*args, **kwargs)


IMPORTANCE_LEVEL = (
    (int(1), '1/5'),
    (int(2), '2/5'),
    (int(3), '3/5'),
)

BOOK_RATING = (
        (Decimal("1.0"), "★☆☆☆☆☆☆☆☆☆ (1/10)"),
        (Decimal("2.0"), "★★☆☆☆☆☆☆☆☆ (2/10)"),
        (Decimal("3.0"), "★★★☆☆☆☆☆☆☆ (3/10)"),
        (Decimal("4.0"), "★★★★☆☆☆☆☆☆ (4/10)"),
        (Decimal("5.0"), "★★★★★☆☆☆☆☆ (5/10)"),
)


class Book(models.Model):
    """Book model"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='пользователь'
    )
    title = models.CharField(
        max_length=255, unique=True, verbose_name='название')
    author = models.ManyToManyField(Author, verbose_name='автор')
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    file = models.FileField(verbose_name='книга', null=False)
    total_pages = models.PositiveIntegerField(verbose_name='количество страниц')

    @property
    def average_rating(self):
        if hasattr(self, '_average_rating'):
            return self._average_rating
        return self.review.aggregate(models.Avg('rating'))

    @property
    def average_review(self):
        if hasattr(self, '_average_review'):
            return self._average_review
        return self.review.aggregate(models.Sum('review'))

    def __str__(self):
        return self.title


class UserBook(models.Model):
    """User book model"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='пользователь'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    importance = models.PositiveSmallIntegerField(choices=IMPORTANCE_LEVEL)
    pages_read = models.PositiveIntegerField(default=0)

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
        super().save(*args, **kwargs)
        self.book.save()


class Review(models.Model):
    """Review model"""
    author = models.ForeignKey(User,
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
        return self.comment
