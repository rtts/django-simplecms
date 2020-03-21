def register(verbose_name):
    import swapper
    Section = swapper.load_model('cms', 'Section')

    '''Decorator to register a specific section type'''
    def wrapper(view):
        Section._cms_views[view.__name__.lower()] = view
        Section.TYPES.append((view.__name__.lower(), verbose_name))
        return view
    return wrapper

# def register_model(verbose_name):
#     '''Decorator to register a section subclass'''
#     def wrapper(model):
#         parent_model = model.__bases__[-1]
#         parent_model.TYPES.append((model.__name__.lower(), verbose_name))
#         return model
#     return wrapper

# def register_view(section_class):
#     '''Decorator to connect a section model to a view class'''
#     def wrapper(model):
#         section_class.view_class = model
#         return model
#     return wrapper
