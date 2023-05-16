from django.contrib import admin

from store.models import Book, UserBookRelation


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "owner")
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "rate")
    list_display_links = ("user", "book")
