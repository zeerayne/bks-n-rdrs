from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import (
    path,
    include
)

urlpatterns = [
    path('api/v1/', include('booksandreaders.api.v1.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]
    urlpatterns += staticfiles_urlpatterns()
