from datetime import datetime
from rest_framework import (
    views,
    viewsets,
    mixins,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_csv import renderers
from .serializers import ReaderSerializer
from .models import (
    Reader,
    Book,
)


class ReaderViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ReaderSerializer
    permission_classes = (AllowAny, )
    authentication_classes = ()

    def get_queryset(self):
        return Reader.objects.all()


class CSVExportView(views.APIView):
    renderer_classes = (renderers.CSVRenderer, )
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @classmethod
    def get_prepared_content(cls):
        readers = Reader.objects.all()
        books = Book.objects.all()
        content = [
                      {
                          'reader_id': reader.id,
                          'reader_name': reader.name,
                          'book_id': None,
                          'book_name': None,
                          'book_isbn': None,
                          'book_reader_id': None,
                      } for reader in readers
                  ] + [
                      {
                          'reader_id': None,
                          'reader_name': None,
                          'book_id': book.id,
                          'book_name': book.name,
                          'book_isbn': book.isbn,
                          'book_reader_id': book.reader_id,
                      } for book in books
                  ]
        return content

    def get(self, request, format=None):
        content = CSVExportView.get_prepared_content()
        datetime_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        return Response(
            content,
            headers={'Content-Disposition': f'attachment; filename="export_{datetime_str}.csv"'},
            content_type='text/csv'
        )
