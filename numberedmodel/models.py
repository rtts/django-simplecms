from django.db import models

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
