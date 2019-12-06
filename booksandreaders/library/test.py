from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_csv.renderers import CSVRenderer
from faker import Faker
from faker.providers import isbn
from .models import (
    Reader,
    Book,
)
from .views import CSVExportView
from .serializers import ReaderSerializer


fake = Faker()
fake.add_provider(isbn)


class LibraryEndpointsWithDataTests(APITestCase):

    def setUp(self):
        self.reader_with_book = Reader.objects.create(name=fake.name())
        self.book_with_reader = Book.objects.create(
            name=fake.text(100).replace('\n', ' '),
            isbn=fake.isbn13(separator='-'),
            reader=self.reader_with_book,
        )
        self.reader_without_book = Reader.objects.create(name=fake.name())
        self.book_without_reader = Book.objects.create(
            name=fake.text(100).replace('\n', ' '),
            isbn=fake.isbn13(separator='-'),
        )

    def tearDown(self):
        self.reader_with_book.delete()
        self.book_with_reader.delete()
        self.reader_without_book.delete()
        self.book_without_reader.delete()

    def test_get_reader_with_book(self):
        url = reverse('reader-detail', args=[self.reader_with_book.id, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, ReaderSerializer(self.reader_with_book).data)

    def test_get_reader_without_book(self):
        url = reverse('reader-detail', args=[self.reader_without_book.id, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, ReaderSerializer(self.reader_without_book).data)

    def test_csv_export(self):
        url = reverse('csv-export')
        response = self.client.get(url, format='csv')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, CSVRenderer().render(CSVExportView.get_prepared_content()))


class LibraryEndpointsWithoutDataTests(APITestCase):

    def test_get_nonexistent_reader(self):
        url = reverse('reader-detail', args=[1, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_empty_csv_export(self):
        url = reverse('csv-export')
        response = self.client.get(url, format='csv')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, CSVRenderer().render(CSVExportView.get_prepared_content()))
