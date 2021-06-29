class EasilyMigratable:
    """
    Mixin for model fields. Prevents the generation of migrations that
    don't affect the database.
    """

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        for field in [
            "blank",
            "choices",
            "editable",
            "help_text",
            "limit_choices_to",
            "related_name",
            "storage",
            "upload_to",
            "validators",
            "verbose_name",
        ]:
            if field in kwargs:
                del kwargs[field]
        return name, path, args, kwargs


class Numbered:
    """
    Mixin for numbered models. Overrides the save() method to
    automatically renumber all instances returned by
    number_with_respect_to()
    """

    def number_with_respect_to(self):
        return self.__class__.objects.all()

    def get_field_name(self):
        return self.__class__._meta.ordering[-1].lstrip("-")

    def _renumber(self):
        """Renumbers the queryset while preserving the instance's number"""

        queryset = self.number_with_respect_to()
        field_name = self.get_field_name()
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
        setattr(self, self.get_field_name(), 9999)  # hack
        self._renumber()
        super().delete(*args, **kwargs)
