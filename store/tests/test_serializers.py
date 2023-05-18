import json

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username="User 1")
        self.user2 = User.objects.create(username="User 2")
        self.user3 = User.objects.create(username="User 3")

        self.book1 = Book.objects.create(name="Test book 1", price=1000, author="Author 1")
        self.book2 = Book.objects.create(name="Test book 2", price=1100, author="Author 2")

        UserBookRelation.objects.create(user=self.user1, book=self.book1, like=True, rate=3)
        UserBookRelation.objects.create(user=self.user2, book=self.book1, like=True, rate=4)
        UserBookRelation.objects.create(user=self.user3, book=self.book1, like=True, rate=4)

        UserBookRelation.objects.create(user=self.user1, book=self.book2, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book2, like=True, rate=1)
        UserBookRelation.objects.create(user=self.user3, book=self.book2, like=False)

    def test_ok(self):
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # rating=Avg("userbookrelation__rate")
        ).order_by("id")
        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                "id": self.book1.id,
                "name": "Test book 1",
                "price": "1000.00",
                "author": "Author 1",
                "annotated_likes": 3,
                "rating": '3.67',
                "readers": [
                    {
                        "username": "User 1",
                        "first_name": "",
                        "last_name": ""
                    },
                    {
                        "username": "User 2",
                        "first_name": "",
                        "last_name": ""
                    },
                    {
                        "username": "User 3",
                        "first_name": "",
                        "last_name": ""
                    }
                ]
            },
            {
                "id": self.book2.id,
                "name": "Test book 2",
                "price": '1100.00',
                "author": "Author 2",
                "annotated_likes": 2,
                "rating": "3.00",
                "readers": [
                    {
                        "username": "User 1",
                        "first_name": "",
                        "last_name": ""
                    },
                    {
                        "username": "User 2",
                        "first_name": "",
                        "last_name": ""
                    },
                    {
                        "username": "User 3",
                        "first_name": "",
                        "last_name": ""
                    }
                ]
            }
        ]
        print(data)
        self.assertEquals(expected_data, data)

