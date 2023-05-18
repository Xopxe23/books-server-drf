import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation


class BooksApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username="Test User")
        self.user2 = User.objects.create(username="Test User 2")
        self.book1 = Book.objects.create(name="Test book 1", price=1000,
                                         author="Author 1", owner=self.user1)
        self.book2 = Book.objects.create(name="Test book 2", price=1100,
                                         author="Author 2", owner=self.user2)

    def test_get(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            "like": True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertTrue(relation.like)
        data2 = {
            "in_bookmarks": True
        }
        json_data2 = json.dumps(data2)
        self.client.patch(url, data=json_data2, content_type='application/json')
        relation2 = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertTrue(relation2.in_bookmarks)
