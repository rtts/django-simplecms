import swapper
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

Page = swapper.load_model('cms', 'Page')
Section = swapper.load_model('cms', 'Section')

class PageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        extra = 1 if self.instance.pk else 2

        self.formsets = [forms.inlineformset_factory(
            parent_model = Page,
            model = Section,
            form = SectionForm,
            extra=extra,
        )(
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
            instance=self.instance,
            form_kwargs={'label_suffix': self.label_suffix},
        )]
        if not self.instance.pk:
            self.formsets[0][0].empty_permitted = False

    def is_valid(self):
        return super().is_valid() and self.formsets[0].is_valid()

    def clean(self):
        super().clean()
        if not self.formsets[0].is_valid():
            self.add_error(None, _('There’s a problem saving one of the sections'))

    def save(self, *args, **kwargs):
        page = super().save()
        formset = self.formsets[0]
        formset.instance = page
        formset.save()
        if page.slug and not page.sections.exists():
            page.delete()
            return None
        return page

    class Meta:
        model = Page
        fields = '__all__'

class SectionForm(forms.ModelForm):
    type = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['DELETE'] = forms.BooleanField(label=_('Delete'), required=False)

        # Repopulate the 'choices' attribute of the type field from
        # the child model.
        self.fields['type'].choices = self._meta.model.TYPES
        self.fields['type'].initial = self._meta.model.TYPES[0][0]

        section = self.instance
        self.formsets = []
        for field in section._meta.get_fields():
            if field.one_to_many:
                extra = 1 if getattr(section, field.name).exists() else 2
                formset = forms.inlineformset_factory(
                    Section, field.related_model,
                    fields='__all__',
                    extra=extra,
                )(
                    instance=section,
                    data=self.data if self.is_bound else None,
                    files=self.files if self.is_bound else None,
                    prefix=f'{self.prefix}-{field.name}',
                    form_kwargs={'label_suffix': self.label_suffix},
                )
                formset.name = field.name
                self.formsets.append(formset)

    def is_valid(self):
        result = super().is_valid()
        if self.is_bound:
            for formset in self.formsets:
                result = result and formset.is_valid()
        return result

    def save(self, commit=True):
        section = super().save(commit=commit)

        if self.cleaned_data['DELETE']:
            section.delete()
            if section.page.slug and not section.page.sections.exists():
                section.page.delete()
            return

        # Explanation: get the content type of the model that the user
        # supplied when filling in this form, and save it's id to the
        # 'polymorphic_ctype_id' field. The next time the object is
        # requested from the database, django-polymorphic will convert
        # it to the correct subclass.
        section.polymorphic_ctype = ContentType.objects.get(
            app_label=section._meta.app_label,
            model=section.type.lower(),
        )

        if commit:
            section.save()
        for formset in self.formsets:
            formset.save(commit=commit)

        return section

    class Meta:
        model = Section
        exclude = ['page']

class ContactForm(forms.Form):
    sender = forms.EmailField(label=_('Your email address'))
    spam_protection = forms.CharField(label=_('Your message'), widget=forms.Textarea())
    message = forms.CharField(label=_('Your message'), widget=forms.Textarea(), initial='Hi there!')

    def save(self, request):
        hostname = request.get_host()
        body = self.cleaned_data.get('spam_protection')
        if len(body.split()) < 7:
            return
        spamcheck = self.cleaned_data.get('message')
        if spamcheck != 'Hi there!':
            return

        email = EmailMessage(
            to = ['info@' + hostname],
            from_email = 'noreply@' + hostname,
            body = body,
            subject = _('Contact form at %(hostname)s.') % {'hostname': hostname},
            headers = {'Reply-To': self.cleaned_data.get('sender')},
        )
        email.send()
