from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def test_get(self):
        book1 = Book.objects.create(name="Test book 1", price=100)
        book2 = Book.objects.create(name="Test book 2", price=100)
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([book1, book2], many=True).data
        print(serializer_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(serializer_data, response.data)
