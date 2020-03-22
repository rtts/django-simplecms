page_class = None
section_class = None
section_types = []
view_per_type = {}

def get_types():
    return section_types

def get_view(section, request):
    return view_per_type[section.type](request)

def get_fields_per_type():
    fields_per_type = {}
    for name, view in view_per_type.items():
        fields_per_type[name] = ['title', 'type', 'number'] + view.fields
    return fields_per_type

