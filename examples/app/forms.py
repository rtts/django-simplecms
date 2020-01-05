from django import forms
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    sender = forms.EmailField(label=_('Your email address'))
    spam_protection = forms.CharField(label=_('Your message'), widget=forms.Textarea())
    message = forms.CharField(label=_('Your message'), widget=forms.Textarea(), initial='Hi there!')

    def save(self, request):
        hostname = request.get_host()
        body = self.cleaned_data.get('spam_protection') # MUHAHA
        if len(body.split()) < 7:
            return
        email = EmailMessage(
            to = ['info@' + hostname],
            from_email = 'noreply@' + hostname,
            body = body,
            subject = _('Contact form at %(hostname)s.') % {'hostname': hostname},
            headers = {'Reply-To': self.cleaned_data.get('sender')},
        )
        email.send()
