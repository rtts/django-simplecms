from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField

# From https://github.com/JaapJoris/django-numberedmodel.git
class NumberedModel(models.Model):
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
                super(NumberedModel, other).save()
            counter += 1
        if not inserted:
            setattr(self, field_name, counter)

    def save(self, *args, **kwargs):
        self._renumber()
        super(NumberedModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(NumberedModel, self).delete(*args, **kwargs)
        self._renumber()

    class Meta:
        abstract = True

class Page(NumberedModel):
    position = models.PositiveIntegerField(_('position'), blank=True)
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), help_text=_('A short identifier to use in URLs'), blank=True, unique=True)
    menu = models.BooleanField(_('visible in menu'), default=True)

    def __str__(self):
        return '{}. {}'.format(self.position, self.title)

    def get_absolute_url(self):
        if self.slug:
            return reverse('cms:page', args=[self.slug])
        else:
            return reverse('cms:homepage')

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ['position']

class Section(NumberedModel):
    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='sections', on_delete=models.PROTECT)
    position = models.PositiveIntegerField(_('position'), blank=True)
    title = models.CharField(_('title'), max_length=255)
    type = models.CharField(_('section type'), max_length=16, default=settings.SECTION_TYPES[0][0], choices=settings.SECTION_TYPES)
    color = models.PositiveIntegerField(_('color'), default=1, choices=settings.SECTION_COLORS)

    content = RichTextField(_('content'), blank=True)
    image = models.ImageField(_('image'), blank=True)
    video = EmbedVideoField(_('video'), blank=True, help_text='Paste a YouTube, Vimeo, or SoundCloud link')
    button_text = models.CharField(_('button text'), max_length=255, blank=True)
    button_link = models.CharField(_('button link'), max_length=255, blank=True)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def __str__(self):
        return '{}. {}'.format(self.position, self.title)

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
        ordering = ['position']

class Config(models.Model):
    TYPES = [
        (10, _('Footer')),
    ]

    parameter = models.PositiveIntegerField(choices=TYPES, unique=True)
    content = RichTextField('Inhoud', blank=True)

    def __str__(self):
        return "{}. {}".format(self.parameter, self.get_parameter_display())

    class Meta:
        verbose_name = _('configuration parameter')
        verbose_name_plural = _('configuration parameters')
        ordering = ['parameter']
