from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.book1 = Book.objects.create(name="Test book 1", price=1000, author="Author 1")
        self.book2 = Book.objects.create(name="Test book 2", price=1100, author="Author 2")
        self.book3 = Book.objects.create(name="Test book 3", price=800, author="Author 1")

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={"search": "Author 1"})
        serializer_data = BookSerializer([self.book1, self.book3], many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={"price": "1100.00"})
        serializer_data = BookSerializer([self.book2], many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={"ordering": "author"})
        serializer_data = BookSerializer([self.book1, self.book3, self.book2], many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(serializer_data, response.data)
