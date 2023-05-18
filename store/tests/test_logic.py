from django.contrib.auth.models import User
from django.test import TestCase

from store.logic import set_rating
from store.models import UserBookRelation, Book


class SetRatingTest(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username="User 1")
        self.user2 = User.objects.create(username="User 2")
        self.user3 = User.objects.create(username="User 3")

        self.book = Book.objects.create(name="Test book 1", price=1000, author="Author 1")

        UserBookRelation.objects.create(user=self.user1, book=self.book, like=True, rate=3)
        UserBookRelation.objects.create(user=self.user2, book=self.book, like=True, rate=4)
        UserBookRelation.objects.create(user=self.user3, book=self.book, like=True, rate=4)

    def test_ok(self):
        set_rating(self.book)
        self.book.refresh_from_db()
        self.assertEquals(str(self.book.rating), "3.67")
