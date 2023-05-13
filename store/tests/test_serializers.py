from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.book1 = Book.objects.create(name="Test book 1", price=1000, author="Author 1")
        self.book2 = Book.objects.create(name="Test book 2", price=1100, author="Author 1")
        self.book3 = Book.objects.create(name="Test book 3", price=800, author="Author 2")

    def test_ok(self):
        data = BookSerializer([self.book1, self.book2, self.book3], many=True).data
        expected_data = [
            {
                "id": self.book1.id,
                "name": "Test book 1",
                "price": '1000.00',
                "author": "Author 1",
            },
            {
                "id": self.book2.id,
                "name": "Test book 2",
                "price": '1100.00',
                "author": "Author 1",
            },
            {
                "id": self.book3.id,
                "name": "Test book 3",
                "price": '800.00',
                "author": "Author 2",
            }
        ]
        self.assertEquals(data, expected_data)
