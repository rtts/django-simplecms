from cms.models import BasePage, BaseSection
from cms.decorators import register_model

class Page(BasePage):
    '''Add custom fields here. Already existing fields: position, title,
    slug, menu

    '''

class Section(BaseSection):
    '''Add custom fields here. Already existing fields: type, position,
    title, color, content, image, video, button_text, button_link

    '''

@register_model('Tekst')
class TextSection(Section):
    fields = ['type', 'position', 'title', 'content']
    class Meta:
        proxy = True

@register_model('Afbeelding')
class ImageSection(Section):
    fields = ['type', 'position', 'title', 'image']
    class Meta:
        proxy = True

@register_model('Contact')
class ContactSection(Section):
    fields = ['type', 'position', 'title']
    class Meta:
        proxy = True
