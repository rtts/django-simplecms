from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from embed_video.fields import EmbedVideoField

from . import fields, mixins


class BasePage(mixins.Numbered, models.Model):
    """Abstract base model for pages."""

    title = fields.CharField(_("page"))
    slug = fields.SlugField(_("slug"), blank=True, unique=True)
    number = fields.PositiveIntegerField(_("number"), blank=True)
    menu = fields.BooleanField(_("visible in menu"), default=True)

    def __str__(self):
        if not self.pk:
            return str(_("New page"))
        return self.title

    def get_absolute_url(self):
        if self.slug:
            return reverse("cms:page", args=[self.slug])
        return reverse("cms:page")

    class Meta:
        abstract = True
        verbose_name = _("page")
        verbose_name_plural = _("pages")
        ordering = ["number"]


class BaseSection(mixins.Numbered, models.Model):
    """Abstract base model for sections"""

    TYPES = []
    title = fields.CharField(_("section"))
    type = fields.CharField(_("type"))
    number = fields.PositiveIntegerField(_("number"), blank=True)
    content = fields.TextField(_("content"), blank=True)
    image = fields.ImageField(_("image"), blank=True)
    video = EmbedVideoField(
        _("video"),
        blank=True,
        help_text=_("Paste a YouTube, Vimeo, or SoundCloud link"),
    )
    href = fields.CharField(_("link"), blank=True)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def get_absolute_url(self):
        return self.page.get_absolute_url() + "#" + slugify(self.title)

    def __str__(self):
        if not self.pk:
            return str(_("New section"))
        elif not self.title:
            return str(_("Untitled"))
        else:
            return self.title

    class Meta:
        abstract = True
        verbose_name = _("section")
        verbose_name_plural = _("sections")
        ordering = ["number"]
