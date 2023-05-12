from django.contrib import admin
from store.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    list_display_links = ("id", "name")
    search_fields = ("name",)
