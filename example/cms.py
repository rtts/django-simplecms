from cms.views import SectionView, SectionFormView
from cms.decorators import section_view
from cms.forms import ContactForm
from django.utils.translation import gettext_lazy as _

@section_view
class Text(SectionView):
    verbose_name = _('Text')
    fields = ['title', 'content']
    template_name = 'app/sections/text.html'

@section_view
class Images(SectionView):
    verbose_name = _('Images')
    fields = ['title', 'images']
    template_name = 'app/sections/images.html'

@section_view
class Video(SectionView):
    verbose_name = _('Video')
    fields = ['title', 'video']
    template_name = 'app/sections/video.html'

@section_view
class Contact(SectionFormView):
    verbose_name = _('Contact')
    fields = ['title']
    form_class = ContactForm
    success_url = '/thanks/'
    template_name = 'app/sections/contact.html'
