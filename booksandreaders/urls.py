from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import (
    path,
    include
)

urlpatterns = [
]

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]
    urlpatterns += staticfiles_urlpatterns()
