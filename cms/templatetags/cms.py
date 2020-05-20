from markdown import markdown as md

from django import template
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from cms import registry

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

@register.simple_tag(takes_context=True)
def editsection(context, inner):
    '''Renders a simple link to edit the current section'''
    section = context['section']
    user = context['request'].user
    app_label = section._meta.app_label
    model_name = section._meta.model_name
    if user.has_perm(f'{app_label}.change_{model_name}'):
        slug = section.page.slug
        number = section.number
        url = reverse('cms:updatesection', args=[slug, number]) if slug else reverse('cms:updatesection', args=[number])
        return mark_safe(f'<a class="edit section" href="{url}">{inner}</a>')
    return ''

@register.simple_tag(takes_context=True)
def editpage(context, inner):
    '''Renders a simple link to edit the current page'''
    page = context['page']
    user = context['request'].user
    app_label = page._meta.app_label
    model_name = page._meta.model_name
    if user.has_perm(f'{app_label}.change_{model_name}'):
        slug = page.slug
        url = reverse('cms:updatepage', args=[slug]) if slug else reverse('cms:updatepage')
        return mark_safe(f'<a class="edit page" href="{url}">{inner}</a>')
    return ''

@register.tag('include_section')
def do_include(parser, token):
    '''Renders the section with its own context'''
    _, section = token.split_contents()
    return IncludeSectionNode(section)

class IncludeSectionNode(template.Node):
    def __init__(self, section):
        self.section = template.Variable(section)
        self.csrf_token = template.Variable('csrf_token')
        self.request = template.Variable('request')
        self.perms = template.Variable('perms')
        super().__init__()

    def render(self, context):
        section = self.section.resolve(context)
        csrf_token = self.csrf_token.resolve(context)
        request = self.request.resolve(context)
        perms = self.perms.resolve(context)

        view = registry.get_view(section, request)
        initial_context = {
            'csrf_token': csrf_token,
            'section': section,
            'request': request,
            'perms': perms,
        }
        if hasattr(section, 'invalid_form'):
            initial_context['form'] = section.invalid_form

        section_context = view.get_context_data(**initial_context)
        t = context.template.engine.get_template(view.template_name)
        return t.render(template.Context(section_context))
