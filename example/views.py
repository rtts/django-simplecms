from django.utils.translation import gettext_lazy as _
from cms.views import SectionView, SectionFormView
from cms.decorators import section_view
from cms.forms import ContactForm

@section_view
class Text(SectionView):
    verbose_name = _('Text')
    fields = ['content']
    template_name = 'text.html'

@section_view
class Images(SectionView):
    verbose_name = _('Image(s)')
    fields = ['images']
    template_name = 'images.html'

@section_view
class Video(SectionView):
    verbose_name = _('Video')
    fields = ['video']
    template_name = 'video.html'

@section_view
class Contact(SectionFormView):
    verbose_name = _('Contact')
    fields = []
    form_class = ContactForm
    success_url = '/thanks/'
    template_name = 'contact.html'
