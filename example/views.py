from cms.decorators import section_view
from cms.forms import ContactForm
from cms.views import SectionFormView, SectionView
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


@section_view
class Text(SectionView):
    verbose_name = _("Text")
    fields = ["content"]
    template_name = "text.html"


@section_view
class Images(SectionView):
    verbose_name = _("Image(s)")
    fields = ["images"]
    template_name = "images.html"


@section_view
class Video(SectionView):
    verbose_name = _("Video")
    fields = ["video"]
    template_name = "video.html"


@section_view
class Contact(SectionFormView):
    verbose_name = _("Contact")
    fields = ["content", "href"]
    form_class = ContactForm
    template_name = "contact.html"

    def form_valid(self, form):
        response = HttpResponse(status=302)
        response["Location"] = form.save(self.object.href)
        return response
