from cms.forms import ContactForm
from cms.views import SectionWithFormView
from cms.decorators import register_view

from .models import *

@register_view(ContactSection)
class ContactFormView(SectionWithFormView):
    form_class = ContactForm
    success_url = '/thanks/'
