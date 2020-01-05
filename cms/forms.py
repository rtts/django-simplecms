import swapper
from django import forms
from django.contrib.contenttypes.models import ContentType

Page = swapper.load_model('cms', 'Page')
Section = swapper.load_model('cms', 'Section')

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'

class SectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Repopulate the 'choices' attribute of the type field from
        # the child model.
        self.fields['type'].choices = self._meta.model.TYPES

    def save(self):
        section = super().save()

        # Explanation: get the content type of the model that the user
        # supplied when filling in this form, and save it's id to the
        # 'polymorphic_ctype_id' field. The next time the object is
        # requested from the database, django-polymorphic will convert
        # it to the correct subclass.
        section.polymorphic_ctype = ContentType.objects.get(
            app_label=section._meta.app_label,
            model=section.type.lower(),
        )

        section.save()
        return section

    class Meta:
        model = Section
        exclude = ['page']
        #field_classes = {
        #    'type': forms.ChoiceField,
        #}

    # There is definitely a bug in Django, since the above 'field_classes' gets
    # ignored entirely. Workaround to force a ChoiceField anyway:
    type = forms.ChoiceField()
