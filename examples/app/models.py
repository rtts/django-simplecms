from cms.models import BaseSection

class Section(BaseSection):
    '''Add custom fields here. Already existing fields: title, color,
    content, image, video, button_text, button_link

    '''

class TextSection(Section):
    fields = ['title', 'content']
    class Meta:
        proxy = True

class ImageSection(Section):
    fields = ['title', 'image']
    class Meta:
        proxy = True

