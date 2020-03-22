views_per_type = {}
page_class = None
section_class = None

def get_view(section, request):
    '''Instantiate the registered view of a section'''
    return views_per_type[section.type](request)

def get_fields_per_type():
    fields_per_type = {}
    for name, view in views_per_type.items():
        fields_per_type[name] = ['title', 'type', 'number'] + view.fields
    return fields_per_type
