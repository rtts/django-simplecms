from django.views.generic import edit
from django.http import HttpResponseRedirect

class SectionView:
    '''Generic section view'''
    template_name = 'cms/sections/section.html'

    def __init__(self, request):
        '''Initialize request attribute'''
        self.request = request

    def get_context_data(self, **kwargs):
        '''Override this to customize a section's context'''
        return kwargs

class SectionFormView(edit.FormMixin, SectionView):
    '''Generic section with associated form'''

    def post(self, request):
        '''Process form'''
        form = self.get_form()
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect(self.get_success_url())
        return form
