"""
Metadata for the application registry.
"""

from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class CmsConfig(AppConfig):
    """
    The `cms` app.
    """

    name = "cms"

    def ready(self):
        """
        When ready, populate the section type registry.
        """

        autodiscover_modules("views")
