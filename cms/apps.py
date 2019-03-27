from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CmsConfig(AppConfig):
    name = 'cms'
    verbose_name = _('Content Management System')
