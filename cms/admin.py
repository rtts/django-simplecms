from django.contrib import admin
from django.utils.text import Truncator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Page, Section, SubSection, Config

class InlineSectionAdmin(admin.StackedInline):
    model = Section
    extra = 0

class InlineSubSectionAdmin(admin.StackedInline):
    model = SubSection
    extra = 0

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [InlineSectionAdmin]

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [InlineSubSectionAdmin]
    list_filter = ['page']

@admin.register(SubSection)
class SubSectionAdmin(admin.ModelAdmin):
    list_filter = ['section', 'section__page']

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_content']
    exclude = ['parameter']

    def get_content(self, obj):
        return mark_safe(Truncator(obj.content).words(50, html=True))
    get_content.short_description = _('content')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False
