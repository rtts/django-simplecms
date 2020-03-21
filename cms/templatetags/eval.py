from markdown import markdown as md
from django import template
from django.utils.safestring import mark_safe

MARKDOWN_EXTENSIONS = ['extra', 'smarty']
register = template.Library()

@register.simple_tag(takes_context=True)
def eval(context, expr):
    '''USE WITH CAUTION!!!

    This template tag runs its argument through Django's templating
    system using the current context, placing all power into the
    hands of the content editors.

    Also, it applies Markdown.

    '''
    result = template.Template(expr).render(context)
    return mark_safe(md(result, extensions=MARKDOWN_EXTENSIONS))
