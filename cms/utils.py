from .models import Config

def get_config(parameter):
    '''Gets or creates the requested parameter.

    '''
    if parameter not in [t[0] for t in Config.TYPES]:
        raise ValueError('Invalid configuration parameter requested')
    (c, created) = Config.objects.get_or_create(parameter=parameter)
    return c.content
