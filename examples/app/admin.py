from django.contrib import admin
from cms.admin import BaseSectionAdmin
from .models import Section

@admin.register(Section)
class SectionAdmin(BaseSectionAdmin):
    pass
