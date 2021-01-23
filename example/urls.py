from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.site.site_header = admin.site.site_title = settings.PROJECT_NAME.replace('_', ' ').title()
urlpatterns = staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', RedirectView.as_view(url='/accounts/login/')),
    path('logout/', RedirectView.as_view(url='/accounts/logout/')),
    path('', include('cms.urls', namespace='cms')),
]
