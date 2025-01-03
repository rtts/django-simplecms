"""
View classes for all possible section types.
"""

from cms.decorators import section_view
from cms.views import ContactSectionFormView, SectionView
from django.utils.translation import gettext_lazy as _


@section_view
class Text(SectionView):
    """
    A section that displays text.
    """

    verbose_name = _("Text")
    template_name = "text.html"
    fields = ["content"]


@section_view
class Images(SectionView):
    """
    A section that displays images.
    """

    verbose_name = _("Image(s)")
    template_name = "images.html"
    fields = ["images"]


@section_view
class Video(SectionView):
    """
    A section that displays a video.
    """

    verbose_name = _("Video")
    template_name = "video.html"
    fields = ["video"]


@section_view
class Contact(ContactSectionFormView):
    """
    A section that displays a contact form.
    """

    verbose_name = _("Contact")
    template_name = "contact.html"
    fields = ["content", "href", "subject"]
