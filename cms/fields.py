from django.db import models
from django.forms import TextInput

from .mixins import EasilyMigratable


class CharField(EasilyMigratable, models.TextField):
    """Variable width CharField."""

    def formfield(self, **kwargs):
        if not self.choices:
            kwargs.update({"widget": TextInput})
        return super().formfield(**kwargs)


class TextField(EasilyMigratable, models.TextField):
    pass


class SlugField(EasilyMigratable, models.SlugField):
    pass


class EmailField(EasilyMigratable, models.EmailField):
    pass


class BooleanField(EasilyMigratable, models.BooleanField):
    pass


class DateField(EasilyMigratable, models.DateField):
    pass


class DateTimeField(EasilyMigratable, models.DateTimeField):
    pass


class PositiveIntegerField(EasilyMigratable, models.PositiveIntegerField):
    pass


class DecimalField(EasilyMigratable, models.DecimalField):
    pass


class JSONField(EasilyMigratable, models.JSONField):
    pass


class FileField(EasilyMigratable, models.FileField):
    pass


class ImageField(EasilyMigratable, models.ImageField):
    pass


class ForeignKey(EasilyMigratable, models.ForeignKey):
    def __init__(self, *args, related_name="+", **kwargs):
        super().__init__(
            *args,
            related_name=related_name,
            **kwargs,
        )


class ManyToManyField(EasilyMigratable, models.ManyToManyField):
    pass


class OneToOneField(EasilyMigratable, models.OneToOneField):
    pass
