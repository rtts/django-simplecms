import json
import swapper

from django.shortcuts import redirect
from django.views.generic import base, detail, edit
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from .forms import PageForm, SectionForm

Page = swapper.load_model('cms', 'Page')
Section = swapper.load_model('cms', 'Section')

class PageView(detail.DetailView):
    '''View of a page with heterogeneous sections'''
    model = Page
    template_name = 'cms/page.html'

    def setup(self, *args, slug='', **kwargs):
        '''Supply a default argument for slug'''
        super().setup(*args, slug=slug, **kwargs)

    def get(self, request, *args, **kwargs):
        '''Instantiate section views and render final response'''
        try:
            page = self.object = self.get_object()
        except Http404:
            if self.request.user.has_perm('cms_page_create'):
                return redirect('cms:updatepage', self.kwargs['slug'])
            raise
        context = self.get_context_data(**kwargs)
        sections = page.sections.all()
        context.update({
            'page': page,
            'sections': sections,
        })
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        '''Call the post() method of the correct section view'''
        try:
            pk = int(self.request.POST.get('section'))
        except:
            return HttpResponseBadRequest()

        page = self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        sections = page.sections.all()
        for section in sections:
            if section.pk == pk:
                view = section.get_view(request)
                result = view.post(request)
                if isinstance(result, HttpResponse):
                    return result
                section.context['form'] = result

        context.update({
            'page': page,
            'sections': sections,
        })
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = Page.objects.filter(menu=True)
        context.update({
            'pages': pages,
        })
        return context

class EditPage(UserPassesTestMixin, edit.ModelFormMixin, base.TemplateResponseMixin, base.View):
    '''Base view with nested forms for editing the page and all its sections'''
    model = Page
    form_class = PageForm
    template_name = 'cms/edit.html'

    def test_func(self):
        '''Only allow users with the correct permissions'''
        return self.request.user.has_perm('cms_page_change')

    def get_form_kwargs(self):
        '''Set the default slug to the current URL for new pages'''
        kwargs = super().get_form_kwargs()
        if 'slug' in self.kwargs:
            kwargs.update({'initial': {'slug': self.kwargs['slug']}})
        return kwargs

    def get_context_data(self, **kwargs):
        '''Populate the fields_per_type dict for use in javascript'''
        context = super().get_context_data(**kwargs)
        context['fields_per_type'] = json.dumps(Section.get_fields_per_type())
        return context

    def get_object(self):
        '''Prevent 404 by serving the new object form'''
        try:
            return super().get_object()
        except Http404:
            return None

    def get(self, *args, **kwargs):
        '''Handle GET requests'''
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, *args, **kwargs):
        '''Handle POST requests'''
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            page = form.save()
            if page:
                return HttpResponseRedirect(page.get_absolute_url())
            return HttpResponseRedirect('/')
        return self.render_to_response(self.get_context_data(form=form, **kwargs))

class CreatePage(EditPage):
    '''View for creating new pages'''
    def get_object(self):
        return Page()

class UpdatePage(EditPage):
    '''View for editing existing pages'''

class EditSection(UserPassesTestMixin, edit.ModelFormMixin, base.TemplateResponseMixin, base.View):
    model = Section
    form_class = SectionForm
    template_name = 'cms/edit.html'

    def test_func(self):
        return self.request.user.has_perm('cms_section_change')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'prefix': 'section',
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields_per_type'] = json.dumps(Section.get_fields_per_type())
        return context

    def get_object(self, queryset=None):
        try:
            self.page = Page.objects.get(slug=self.kwargs['slug'])
        except Page.DoesNotExist:
            raise Http404()
        return self.get_section()

    def get_section(self):
        try:
            section = self.page.sections.get(number=self.kwargs['number'])
        except Section.DoesNotExist:
            raise Http404()
        return section

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            section = form.save()
            if section:
                return HttpResponseRedirect(section.get_absolute_url())
            elif self.page.sections.exists():
                return HttpResponseRedirect(self.page.get_absolute_url())
            else:
                return HttpResponseRedirect('/')
        return self.render_to_response(self.get_context_data(form=form, **kwargs))

class CreateSection(EditSection):
    def get_section(self):
        return Section(page=self.page)

class UpdateSection(EditSection):
    pass
