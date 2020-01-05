def register_model(verbose_name):
    '''Decorator to register a section subclass'''
    def wrapper(model):
        parent_model = model.__bases__[-1]
        parent_model.TYPES.append((model.__name__.lower(), verbose_name))
        return model
    return wrapper

def register_view(section_class):
    '''Decorator to connect a section model to a view class'''
    def wrapper(model):
        section_class.view_class = model
        return model
    return wrapper
