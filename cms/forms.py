from urllib.parse import quote

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from . import registry


class PageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        self.formsets = [
            forms.inlineformset_factory(
                parent_model=registry.page_class,
                model=registry.section_class,
                form=SectionForm,
                extra=1,
            )(
                data=self.data if self.is_bound else None,
                files=self.files if self.is_bound else None,
                instance=self.instance,
            )
        ]
        self.formsets[0][0].empty_permitted = True

    def is_valid(self):
        return super().is_valid() and self.formsets[0].is_valid()

    def has_changed(self):
        return super().has_changed() or self.formsets[0].has_changed()

    def clean(self):
        super().clean()
        if not self.formsets[0].is_valid():
            self.add_error(None, repr(self.formsets[0].errors))

    def save(self, *args, **kwargs):
        page = super().save()
        formset = self.formsets[0]
        formset.instance = page
        formset.save()
        return page

    class Meta:
        model = registry.page_class
        fields = "__all__"


class SectionForm(forms.ModelForm):
    type = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["DELETE"] = forms.BooleanField(label=_("Delete"), required=False)
        self.fields["type"].choices = registry.get_types()
        self.fields["type"].initial = registry.get_types()[0][0]

        # Populate the 'formsets' attribute if the Section was
        # extendend with one_to_many fields
        self.formsets = []
        for field in self.instance._meta.get_fields():
            if field.one_to_many:
                formset = forms.inlineformset_factory(
                    parent_model=registry.section_class,
                    model=field.related_model,
                    fields="__all__",
                    extra=1,
                )(
                    instance=self.instance,
                    data=self.data if self.is_bound else None,
                    files=self.files if self.is_bound else None,
                    prefix=f"{self.prefix}-{field.name}",
                    form_kwargs={"label_suffix": self.label_suffix},
                )
                formset.name = field.name
                self.formsets.append(formset)

    def is_valid(self):
        result = super().is_valid()
        for formset in self.formsets:
            result = result and formset.is_valid()  # AND
        return result

    def has_changed(self):
        result = super().has_changed()
        for formset in self.formsets:
            result = result or formset.has_changed()  # OR
        return result

    def save(self, commit=True):
        section = super().save(commit=commit)

        if self.cleaned_data["DELETE"]:
            section.delete()
            if section.page.slug and not section.page.sections.exists():
                section.page.delete()
            return
        elif commit:
            section.save()

        for formset in self.formsets:
            formset.save(commit=commit)

        return section

    class Meta:
        model = registry.section_class
        exclude = ["page"]


class ContactForm(forms.Form):
    """
    Spam-resistant contact form.
    """

    body = forms.CharField(label=_("Message"), widget=forms.Textarea(), required=False)

    def save(self, address):
        """
        Return a mailto: link.
        """

        subject = quote(settings.CONTACT_FORM_EMAIL_SUBJECT, safe="")
        body = quote(self.cleaned_data.get("body"), safe="")
        return f"mailto:{address}?subject={subject}&body={body}"
