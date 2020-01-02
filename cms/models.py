'''CMS Models'''

import swapper

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.forms import TextInput, Select
from django.utils.translation import gettext_lazy as _
from embed_video.fields import EmbedVideoField
from polymorphic.models import PolymorphicModel
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_NULL

from numberedmodel.models import NumberedModel

class VarCharField(models.TextField):
    '''Variable width CharField'''
    def formfield(self, **kwargs):
        kwargs.update({'widget': TextInput})
        return super().formfield(**kwargs)

class VarCharChoiceField(models.TextField):
    '''Variable width CharField with choices'''
    def formfield(self, **kwargs):
        kwargs.update({'widget': Select})
        return super().formfield(**kwargs)

class BasePage(NumberedModel):
    '''Abstract base model for pages'''
    slug = models.SlugField(_('slug'), help_text=_('A short identifier to use in URLs'), blank=True, unique=True)
    title = VarCharField(_('title'))
    position = models.PositiveIntegerField(_('position'), blank=True)
    menu = models.BooleanField(_('visible in menu'), default=True)

    def __str__(self):
        if not self.pk:
            return str(_('New page'))
        return self.title

    def get_absolute_url(self):
        if self.slug:
            return reverse('cms:page', args=[self.slug])
        return reverse('cms:page')

    class Meta:
        abstract = True
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ['position']

class BaseSection(NumberedModel, PolymorphicModel):
    '''Abstract base model for sections'''
    TYPES = []
    page = models.ForeignKey(swapper.get_model_name('cms', 'Page'), verbose_name=_('page'), related_name='sections', on_delete=models.PROTECT)
    type = VarCharChoiceField(_('type'), default='', choices=TYPES)
    title = VarCharField(_('title'), blank=True)
    position = models.PositiveIntegerField(_('position'), blank=True)
    color = models.PositiveIntegerField(_('color'), default=1, choices=settings.SECTION_COLORS)
    content = MarkdownField(_('content'), rendered_field='content_rendered', validator=VALIDATOR_NULL, use_admin_editor=False, blank=True)
    content_rendered = RenderedMarkdownField()
    image = models.ImageField(_('image'), blank=True)
    video = EmbedVideoField(_('video'), blank=True, help_text=_('Paste a YouTube, Vimeo, or SoundCloud link'))
    button_text = VarCharField(_('button text'), blank=True)
    button_link = VarCharField(_('button link'), blank=True)

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

class Page(BasePage):
    '''Swappable page model'''
    class Meta(BasePage.Meta):
        swappable = swapper.swappable_setting('cms', 'Page')

class Section(BaseSection):
    '''Swappable section model'''
    class Meta(BaseSection.Meta):
        swappable = swapper.swappable_setting('cms', 'Section')
