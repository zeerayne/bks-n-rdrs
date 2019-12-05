from rest_framework import serializers
from .models import Book, Reader


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'isbn']


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ['id', 'name', 'books']
        depth = 1

    books = BookSerializer(many=True, read_only=True)
