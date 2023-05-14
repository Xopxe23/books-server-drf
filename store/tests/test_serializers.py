import json

from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test User")
        self.book1 = Book.objects.create(name="Test book 1", price=1000, author="Author 1", owner=self.user)
        self.book2 = Book.objects.create(name="Test book 2", price=1100, author="Author 1", owner=self.user)
        self.book3 = Book.objects.create(name="Test book 3", price=800, author="Author 2", owner=self.user)

    def test_ok(self):
        data = BookSerializer([self.book1, self.book2, self.book3], many=True).data
        expected_data = json.dumps([
            {
                "id": self.book1.id,
                "name": "Test book 1",
                "price": "1000.00",
                "author": "Author 1",
                "owner": self.user.id
            },
            {
                "id": self.book2.id,
                "name": "Test book 2",
                "price": '1100.00',
                "author": "Author 1",
                "owner": self.user.id
            },
            {
                "id": self.book3.id,
                "name": "Test book 3",
                "price": "800.00",
                "author": "Author 2",
                "owner": self.user.id
            }
        ])
        data_json = json.dumps(data)
        self.assertEquals(expected_data, data_json)
