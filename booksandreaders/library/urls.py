from django.urls import (
    path,
    include,
)
from rest_framework import routers
from .views import (
    ReaderViewSet,
    CSVExportView,
)

router = routers.SimpleRouter()
router.register('reader', ReaderViewSet, basename='reader')

urlpatterns = [
    path('', include(router.urls)),
    path('export/', CSVExportView.as_view()),
]
