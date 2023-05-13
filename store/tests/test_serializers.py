from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name="Test book 1", price=100)
        book2 = Book.objects.create(name="Test book 2", price=50)
        data = BookSerializer([book1, book2], many=True).data
        expected_data = [
            {
                "id": book1.id,
                "name": "Test book 1",
                "price": '100.00',
            },
            {
                "id": book2.id,
                "name": "Test book 2",
                "price": '50.00',
            }
        ]
        self.assertEquals(data, expected_data)
