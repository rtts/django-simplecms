from cms import registry

def page_model(cls):
    '''Decorator to register the Page model'''
    registry.page_class = cls
    return cls

def section_model(cls):
    '''Decorator to register the Section model'''
    registry.section_class = cls
    return cls

def section_view(cls):
    '''Decorator to register a view for a specific section'''
    registry.view_per_type[cls.__name__.lower()] = cls
    registry.section_types.append((cls.__name__.lower(), cls.verbose_name))
    return cls
