import os
from sass import compile
from django.conf import settings

def locate(filename):
    for path, dirs, files in os.walk(os.getcwd(), followlinks=True):
        for f in files:
            if f == filename:
                return os.path.join(path, filename)

class SassMiddleware:
    '''Simple SASS middleware that intercepts requests for .css files and
    tries to compile the corresponding SCSS file.

    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG and request.path.endswith('.css'):
            css_file = request.path.rsplit('/',1)[1]
            sass_file = css_file[:-4]
            sass_path = locate(sass_file)
            if sass_path and os.path.exists(sass_path):
                css_path = sass_path + '.css'
                map_path = css_path + '.map'
                css = compile(filename=sass_path, output_style='nested')
                css, mapping = compile(filename=sass_path, source_map_filename=map_path)
                with open(css_path, 'w') as f:
                    f.write(css)
                with open(map_path, 'w') as f:
                    f.write(mapping)

        response = self.get_response(request)
        return response
