import json
import swapper

from django.shortcuts import redirect
from django.views.generic import base, detail, edit
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import UserPassesTestMixin

from .decorators import register_view
from .forms import PageForm, SectionForm

Page = swapper.load_model('cms', 'Page')
Section = swapper.load_model('cms', 'Section')

@register_view(Section)
class SectionView:
    '''Generic section view'''
    template_name = 'cms/sections/section.html'

    def setup(self, request, section):
        '''Initialize request and section attributes'''
        self.request = request
        self.section = section

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

class PageView(detail.DetailView):
    '''View of a page with heterogeneous (polymorphic) sections'''
    model = Page
    template_name = 'cms/page.html'

    def setup(self, *args, slug='', **kwargs):
        '''Supply a default argument for slug'''
        super().setup(*args, slug=slug, **kwargs)

    def initialize_section(self, section):
        section.view = section.__class__.view_class()
        section.view.setup(self.request, section)
        section.context = section.view.get_context_data(
            request = self.request,
            section = section,
        )

    def get(self, request, *args, **kwargs):
        '''Initialize sections and render final response'''
        try:
            page = self.object = self.get_object()
        except Http404:
            if self.request.user.has_perm('cms_page_create'):
                return redirect('cms:updatepage', self.kwargs['slug'])
            else:
                raise
        context = self.get_context_data(**kwargs)
        sections = page.sections.all()
        for section in sections:
            self.initialize_section(section)
        context.update({
            'page': page,
            'sections': sections,
        })
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        '''Initialize sections and call the post() function of the correct
        section view'''
        try:
            pk = int(self.request.POST.get('section'))
        except:
            return HttpResponseBadRequest()

        page = self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        sections = page.sections.all()
        for section in sections:
            self.initialize_section(section)
            if section.pk == pk:
                result = section.view.post(request)
                if isinstance(result, HttpResponseRedirect):
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
    model = Page
    form_class = PageForm
    template_name = 'cms/edit.html'

    def test_func(self):
        app, model = swapper.get_model_name('cms', 'page').lower().split('.')
        return self.request.user.has_perm('f{app}_{model}_change')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'slug' in self.kwargs:
            kwargs.update({'initial': {'slug': self.kwargs['slug']}})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields_per_type = {}
        for model, _ in Section.TYPES:
            ctype = ContentType.objects.get(
                app_label = Section._meta.app_label,
                model = model.lower(),
            )
            fields_per_type[ctype.model] = ['type', 'number'] + ctype.model_class().fields

        context.update({
            'fields_per_type': json.dumps(fields_per_type),
        })
        return context

    def get_object(self):
        '''Prevent 404 by serving the new object form'''
        try:
            return super().get_object()
        except Http404:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            page = form.save()
            if page:
                return HttpResponseRedirect(page.get_absolute_url())
            return HttpResponseRedirect('/')
        return self.render_to_response(self.get_context_data(form=form))

class CreatePage(EditPage):
    def get_object(self):
        return Page()

class UpdatePage(EditPage):
    pass

class EditSection(UserPassesTestMixin, edit.ModelFormMixin, base.TemplateResponseMixin, base.View):
    model = Section
    form_class = SectionForm
    template_name = 'cms/edit.html'

    def test_func(self):
        app, model = swapper.get_model_name('cms', 'section').lower().split('.')
        return self.request.user.has_perm('f{app}_{model}_change')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'prefix': 'section',
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields_per_type = {}
        for model, _ in Section.TYPES:
            ctype = ContentType.objects.get(
                app_label = Section._meta.app_label,
                model = model.lower(),
            )
            fields_per_type[ctype.model] = ['type', 'number'] + ctype.model_class().fields

        context.update({
            'fields_per_type': json.dumps(fields_per_type),
        })
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
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
        return self.render_to_response(self.get_context_data(form=form))

class CreateSection(EditSection):
    def get_section(self):
        return Section(page=self.page)

class UpdateSection(EditSection):
    pass
