import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test User")
        self.user2 = User.objects.create(username="Test User 2")
        self.book1 = Book.objects.create(name="Test book 1", price=1000,
                                         author="Author 1", owner=self.user)
        self.book2 = Book.objects.create(name="Test book 2", price=1100,
                                         author="Author 2", owner=self.user)
        self.book3 = Book.objects.create(name="Test book 3", price=800,
                                         author="Author 1", owner=self.user)

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

    def test_create_book(self):
        self.assertEquals(Book.objects.all().count(), 3)
        url = reverse("book-list")
        data = {
            "name": "Test book 1",
            "price": 700,
            "author": "Test Author"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEquals(Book.objects.last().owner, self.user)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Book.objects.all().count(), 4)

    def test_update_book(self):
        url = reverse("book-detail", args=(self.book1.id,))
        data = {
            "name": self.book1.name,
            "price": 500,
            "author": self.book1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEquals(self.book1.price, 500)

    def test_update_book_not_owner(self):
        url = reverse("book-detail", args=(self.book1.id,))
        data = {
            "name": self.book1.name,
            "price": 500,
            "author": self.book1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.book1.refresh_from_db()
        self.assertEquals(self.book1.price, 1000)

    def test_update_book_not_owner_but_staff(self):
        self.user2 = User.objects.create(username="Test User 2", is_staff=True)
        url = reverse("book-detail", args=(self.book1.id,))
        data = {
            "name": self.book1.name,
            "price": 500,
            "author": self.book1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEquals(self.book1.price, 500)
