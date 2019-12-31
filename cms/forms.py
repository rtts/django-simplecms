from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Page

import swapper
Section = swapper.load_model('cms', 'Section')

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'

class SectionForm(forms.ModelForm):
    def save(self):
        section = super().save()
        app_label = section._meta.app_label
        model = section.type

        # Explanation: we'll get the content type of the model that
        # the user supplied when filling in this form, and save it's
        # id to the 'polymorphic_ctype_id' field. This way, the next
        # time the object is requested from the database,
        # django-polymorphic will automatically convert it to the
        # correct subclass. Brilliant!
        section.polymorphic_ctype = ContentType.objects.get(
            app_label=section._meta.app_label,
            model=section.type.lower(),
        )

        section.save()
        return section

    class Meta:
        model = Section
        exclude = ['page']
