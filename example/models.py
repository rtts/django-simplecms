from django.db import models
from django.utils.translation import gettext_lazy as _
from cms.models import BasePage, BaseSection
from cms.decorators import page_model, section_model

@page_model
class Page(BasePage):
    '''Add custom fields here. Already existing fields: title, slug,
    number, menu

    '''

@section_model
class Section(BaseSection):
    '''Add custom fields here. Already existing fields: title, type,
    number, content, image, video, href

    '''
    page = models.ForeignKey(Page, related_name='sections', on_delete=models.PROTECT)

class SectionImage(models.Model):
    section = models.ForeignKey(Section, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_('Image'))

    class Meta:
        ordering = ['pk']
