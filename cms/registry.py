"""
Registry that is populated at startup time by the decorators.
"""

page_class = None
section_class = None
section_types = []
view_per_type = {}


def get_types():
    """
    Return the available section types as tuples to be used for
    form field choices.
    """

    return section_types


def get_view(section, request):
    """
    Given a section instance and a request, return the view class
    that is registered to render that section.
    """

    return view_per_type[section.type](request)


def get_fields_per_type():
    """
    Return a dictionary with the editable fields of each section.
    This is used by the JS to show the the relevant form fields.
    """

    fields_per_type = {}
    for name, view in view_per_type.items():
        fields_per_type[name] = ["title", "type", "number"] + view.fields
    return fields_per_type
