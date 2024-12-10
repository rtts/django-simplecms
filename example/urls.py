"""
URLs.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = (
    staticfiles_urlpatterns()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + [
        path("admin/", admin.site.urls),
        path("accounts/", include("django.contrib.auth.urls")),
        path("", include("cms.urls", namespace="cms")),
    ]
)
