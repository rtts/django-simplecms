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
        extra = 1 if self.instance.pk else 2
        self.formsets = [forms.inlineformset_factory(
            parent_model = Page,
            model = Section,
            form = SectionForm,
            formset = BaseSectionFormSet,
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
        if not self.instance and not self.formsets[0].has_changed():
            self.add_error(None, _('You can’t save a new page without adding any sections!'))

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

        # Repopulate the 'choices' attribute of the type field from
        # the child model.
        self.fields['type'].choices = self._meta.model.TYPES
        self.fields['type'].initial = self._meta.model.TYPES[0][0]

    def delete(self):
        instance = super().save()
        instance.delete()

    def save(self, commit=True):
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

        if commit:
            section.save()
        return section

    core_field_names = ['title', 'type', 'number', 'content', 'image', 'video', 'href']

    def core_fields(self):
        return [field for field in self.visible_fields() if field.name in self.core_field_names]

    def extra_fields(self):
        return [field for field in self.visible_fields() if field.name not in self.core_field_names]

    class Meta:
        model = Section
        exclude = ['page']

class BaseSectionFormSet(forms.BaseInlineFormSet):
    '''If a swappable Section model defines one-to-many fields, (i.e. has
    foreign keys pointing to it) formsets will be generated for the
    related models and stored in the form.formsets array.

    Based on this logic for nested formsets:
    https://www.yergler.net/2013/09/03/nested-formsets-redux/

    Typical usecases could be:
    - an images section that displays multiple images
    - a column section that displays separate colums
    - a calendar section that displays calendar events
    - etc...

    '''
    def add_fields(self, form, index):
        super().add_fields(form, index)
        section = form.instance
        form.formsets = []
        for field in section._meta.get_fields():
            if field.one_to_many:
                extra = 1 if getattr(section, field.name).exists() else 2

                formset = forms.inlineformset_factory(
                    Section, field.related_model,
                    fields='__all__',
                    extra=extra,
                )(
                    instance=section,
                    data=form.data if self.is_bound else None,
                    files=form.files if self.is_bound else None,
                    prefix=f'{form.prefix}-{field.name}',
                    form_kwargs=self.form_kwargs,
                )
                formset.name = field.name
                form.formsets.append(formset)

    def is_valid(self):
        result = super().is_valid()
        if self.is_bound:
            for form in self.forms:
                for formset in form.formsets:
                    result = result and formset.is_valid()
        return result

    def save(self, commit=True):
        result = super().save(commit=commit)
        for form in self:
            for formset in form.formsets:
                formset.save(commit=commit)
        return result

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
