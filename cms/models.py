import swapper
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField
from polymorphic.models import PolymorphicModel

from numberedmodel.models import NumberedModel

class VarCharField(models.TextField):
    def formfield(self, **kwargs):
        kwargs.update({'widget': TextInput})
        return super().formfield(**kwargs)

class Page(NumberedModel):
    position = models.PositiveIntegerField(_('position'), blank=True)
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), help_text=_('A short identifier to use in URLs'), blank=True, unique=True)
    menu = models.BooleanField(_('visible in menu'), default=True)

    def __str__(self):
        if not self.pk:
            return str(_('New page'))
        else:
            return self.title

    def get_absolute_url(self):
        if self.slug:
            return reverse(settings.PAGE_URL_PATTERN, args=[self.slug])
        else:
            return reverse(settings.PAGE_URL_PATTERN)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ['position']

choices = settings.SECTION_TYPES
class BaseSection(NumberedModel, PolymorphicModel):
    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='sections', on_delete=models.PROTECT)
    type = models.CharField(_('section type'), max_length=16, default=choices[0][0], choices=choices)

    position = models.PositiveIntegerField(_('position'), blank=True)
    title = models.CharField(_('title'), max_length=255, blank=True)
    color = models.PositiveIntegerField(_('color'), default=1, choices=settings.SECTION_COLORS)

    content = RichTextField(_('content'), blank=True)
    image = models.ImageField(_('image'), blank=True)
    video = EmbedVideoField(_('video'), blank=True, help_text=_('Paste a YouTube, Vimeo, or SoundCloud link'))
    button_text = models.CharField(_('button text'), max_length=255, blank=True)
    button_link = models.CharField(_('button link'), max_length=255, blank=True)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def __str__(self):
        if not self.pk:
            return str(_('New section'))
        elif not self.title:
            return str(_('Untitled'))
        else:
            return self.title

    class Meta:
        abstract = True
        verbose_name = _('section')
        verbose_name_plural = _('sections')
        ordering = ['position']
        #app_label = 'cms'

class Section(BaseSection):
    class Meta:
        swappable = swapper.swappable_setting('cms', 'Section')

class Config(models.Model):
    TYPES = [
        (10, _('Footer')),
    ]

    parameter = models.PositiveIntegerField(choices=TYPES, unique=True)
    content = RichTextField(_('content'), blank=True)

    def __str__(self):
        return "{}. {}".format(self.parameter, self.get_parameter_display())

    class Meta:
        verbose_name = _('configuration parameter')
        verbose_name_plural = _('configuration parameters')
        ordering = ['parameter']
