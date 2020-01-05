from markdown import markdown as md
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

EXTENSIONS = getattr(settings, 'MARKDOWN_EXTENSIONS', [])

register = template.Library()

@register.filter(is_safe=True)
def markdown(value):
    '''Runs Markdown over a given value

    '''
    return mark_safe(md(value, extensions=EXTENSIONS))
