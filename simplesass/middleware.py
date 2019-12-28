import os
from django.conf import settings
from django.apps import apps
from sass import compile

class SimpleSassMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG and request.path.endswith('.css'):
            _, staticdir, appname, css_file = request.path.split('/', maxsplit=3)
            app_path = apps.get_app_config(appname).path
            sass_file = css_file[:-4]
            css_path = os.path.join(app_path, staticdir, appname, css_file)
            sass_path = os.path.join(app_path, staticdir, appname, sass_file)
            map_path = css_path + '.map'
            if os.path.exists(sass_path):
                css = compile(filename=sass_path, output_style='nested')
                css, mapping = compile(filename=sass_path, source_map_filename=map_path)
                with open(css_path, 'w') as f:
                    f.write(css)
                with open(map_path, 'w') as f:
                    f.write(mapping)

        response = self.get_response(request)
        return response
