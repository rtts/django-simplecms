from cms.views import SectionView, SectionFormView
from cms.decorators import register_view

from .models import *
from .forms import ContactForm

@register_view(TextSection)
class TextView(SectionView):
    template_name = 'app/sections/text.html'

@register_view(ButtonSection)
class ButtonView(SectionView):
    template_name = 'app/sections/button.html'

@register_view(ImageSection)
class ImageView(SectionView):
    template_name = 'app/sections/image.html'

@register_view(VideoSection)
class VideoView(SectionView):
    template_name = 'app/sections/video.html'

@register_view(ContactSection)
class ContactFormView(SectionFormView):
    form_class = ContactForm
    success_url = '/thanks/'
    template_name = 'app/sections/contact.html'
