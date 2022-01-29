from cms.decorators import page_model, section_model
from cms.models import BasePage, BaseSection
from django.db import models
from django.utils.translation import gettext_lazy as _


@page_model
class Page(BasePage):
    pass


@section_model
class Section(BaseSection):
    page = models.ForeignKey(Page, related_name="sections", on_delete=models.PROTECT)


class SectionImage(models.Model):
    section = models.ForeignKey(
        Section, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(_("Image"))

    class Meta:
        ordering = ["pk"]
