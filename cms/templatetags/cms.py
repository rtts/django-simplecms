from django import template

register = template.Library()

@register.tag('include_section')
def do_include(parser, token):
    '''Renders the section with its own context

    '''
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
        view = section.get_view(request)
        section_context = view.get_context_data(
            csrf_token=csrf_token,
            section=section,
            request=request,
            perms=perms,
        )
        t = context.template.engine.get_template(view.template_name)
        return t.render(template.Context(section_context))
