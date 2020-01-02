from cms.models import *

class Page(BasePage):
    '''Add custom fields here. Already existing fields: position, title,
    slug, menu

    '''

class Section(BaseSection):
    '''Add custom fields here. Already existing fields: type, position,
    title, color, content, image, video, button_text, button_link

    '''

@register('Tekst')
class TextSection(Section):
    fields = ['type', 'position', 'title', 'content']
    class Meta:
        proxy = True

@register('Afbeelding')
class ImageSection(Section):
    fields = ['type', 'position', 'title', 'image']
    class Meta:
        proxy = True
