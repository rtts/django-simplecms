import swapper
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

Page = swapper.load_model('cms', 'Page')
Section = swapper.load_model('cms', 'Section')

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

    class Meta:
        model = Section
        exclude = ['page']
        #field_classes = {
        #    'type': forms.ChoiceField,
        #}

    # There is definitely a bug in Django, since the above 'field_classes' gets
    # ignored entirely. Workaround to force a ChoiceField anyway:
    type = forms.ChoiceField()

SectionFormSet = inlineformset_factory(Page, Section, form=SectionForm, extra=1)
