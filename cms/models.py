import swapper

from django.db import models
from django.urls import reverse
from django.forms import TextInput, Select
from django.utils.translation import gettext_lazy as _
from embed_video.fields import EmbedVideoField
from polymorphic.models import PolymorphicModel

class VarCharField(models.TextField):
    '''Variable width CharField'''
    def formfield(self, **kwargs):
        kwargs.update({'widget': TextInput})
        return super().formfield(**kwargs)

class Numbered:
    '''Mixin for numbered models. Overrides the save() method to
    automatically renumber all instances returned by
    number_with_respect_to()

    '''
    def number_with_respect_to(self):
        return self.__class__.objects.all()

    def _renumber(self):
        '''Renumbers the queryset while preserving the instance's number'''

        queryset = self.number_with_respect_to()
        field_name = self.__class__._meta.ordering[-1].lstrip('-')
        this_nr = getattr(self, field_name)
        if this_nr is None:
            this_nr = len(queryset) + 1

        # The algorithm: loop over the queryset and set each object's
        # number to the counter. When an object's number equals the
        # number of this instance, set this instance's number to the
        # counter, increment the counter by 1, and finish the loop
        counter = 1
        inserted = False
        for other in queryset.exclude(pk=self.pk):
            other_nr = getattr(other, field_name)
            if counter >= this_nr and not inserted:
                setattr(self, field_name, counter)
                inserted = True
                counter += 1
            if other_nr != counter:
                setattr(other, field_name, counter)
                super(Numbered, other).save()
            counter += 1
        if not inserted:
            setattr(self, field_name, counter)

    def save(self, *args, **kwargs):
        self._renumber()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self._renumber()

class BasePage(Numbered, models.Model):
    '''Abstract base model for pages'''
    title = VarCharField(_('page'))
    slug = models.SlugField(_('slug'), blank=True, unique=True)
    number = models.PositiveIntegerField(_('number'), blank=True)
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
        ordering = ['number']

class BaseSection(Numbered, PolymorphicModel):
    '''Abstract base model for sections'''
    TYPES = [] # Will be populated by @register_model()
    page = models.ForeignKey(swapper.get_model_name('cms', 'Page'), verbose_name=_('page'), related_name='sections', on_delete=models.PROTECT)
    title = VarCharField(_('section'))
    type = VarCharField(_('type'))
    number = models.PositiveIntegerField(_('number'), blank=True)

    content = models.TextField(_('content'), blank=True)
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
        ordering = ['number']

class Page(BasePage):
    '''Swappable page model'''
    class Meta(BasePage.Meta):
        swappable = swapper.swappable_setting('cms', 'Page')

class Section(BaseSection):
    '''Swappable section model'''
    class Meta(BaseSection.Meta):
        swappable = swapper.swappable_setting('cms', 'Section')
