from django.db import models
from cms.models import BasePage, BaseSection
from django.utils.translation import gettext_lazy as _

class Page(BasePage):
    '''Add custom fields here. Already existing fields: title, slug,
    number, menu

    '''

class Section(BaseSection):
    '''Add custom fields here. Already existing fields: title, type,
    number, content, image, video, href

    '''

class SectionImage(models.Model):
    section = models.ForeignKey(Section, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_('Image'))

    class Meta:
        ordering = ['pk']
