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
        super().__init__()

    def render(self, context):
        section = self.section.resolve(context)
        template_name = section.view.template_name
        if template_name is None:
            raise ValueError(f'{section} view has no template_name attribute')
        csrf_token = self.csrf_token.resolve(context)
        if not hasattr(section, 'context'):
            raise ValueError(dir(section))
        section.context.update({'csrf_token': csrf_token})
        t = context.template.engine.get_template(template_name)
        return t.render(template.Context(section.context))
