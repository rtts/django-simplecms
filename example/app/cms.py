import cms
from cms.forms import ContactForm
from django.utils.translation import gettext_lazy as _

@cms.register(_('Text'))
class Text(cms.SectionView):
    fields = ['title', 'content']
    template_name = 'app/sections/text.html'

@cms.register(_('Images'))
class Images(cms.SectionView):
    fields = ['title', 'images']
    template_name = 'app/sections/images.html'

@cms.register(_('Video'))
class Video(cms.SectionView):
    fields = ['title', 'video']
    template_name = 'app/sections/video.html'

@cms.register(_('Contact'))
class Contact(cms.SectionFormView):
    fields = ['title']
    form_class = ContactForm
    success_url = '/thanks/'
    template_name = 'app/sections/contact.html'
