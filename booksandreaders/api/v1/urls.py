from django.urls import (
    path,
    include
)


urlpatterns = [
    path('library/', include('booksandreaders.library.urls')),
]
