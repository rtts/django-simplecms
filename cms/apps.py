from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import autodiscover_modules

class CmsConfig(AppConfig):
    name = 'cms'
    verbose_name = _('Content Management System')

    def ready(self):
        autodiscover_modules('views')
