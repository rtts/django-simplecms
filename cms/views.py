'''CMS Views'''

import json
import swapper

from django.views import generic
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from .decorators import register_view
from .forms import PageForm, SectionForm
from .utils import get_config

Page = swapper.load_model('cms', 'Page')
Section = swapper.load_model('cms', 'Section')

@register_view(Section)
class SectionView:
    '''Generic section view'''
    def get(self, request, section):
        '''Override this to add custom attributes to a section'''
        return section

class SectionWithFormView(SectionView):
    '''Generic section with associated form'''
    form_class = None
    success_url = None

    def get_form_class(self):
        '''Return the form class to use in this view.'''
        if self.form_class:
            return self.form_class
        raise ImproperlyConfigured(
            'Either specify formclass attribute or override get_form_class()')

    def get_success_url(self):
        '''Return the URL to redirect to after processing a valid form.'''
        if self.success_url:
            return self.success_url
        raise ImproperlyConfigured(
            'Either specify success_url attribute or override get_success_url()')

    def get(self, request, section):
        '''Add form to section'''
        form = self.get_form_class()()
        section.form = form
        return section

    def post(self, request, section):
        '''Process form'''
        form = self.get_form_class()(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            return redirect(self.get_success_url())
        section.form = form
        return section

class MenuMixin:
    '''Add pages and footer to template context'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = Page.objects.filter(menu=True)
        footer = get_config(10)
        context.update({
            'pages': pages,
            'footer': footer,
        })
        return context

class MemoryMixin:
    '''Remember the previous page in session'''
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.session['previous_url'] = request.path
        return super().dispatch(request, *args, **kwargs)

class PageView(MenuMixin, MemoryMixin, generic.DetailView):
    '''View of a page with heterogeneous (polymorphic) sections'''
    model = Page
    template_name = 'cms/page.html'

    def setup(self, *args, slug='', **kwargs):
        '''Supply a default argument for slug'''
        super().setup(*args, slug=slug, **kwargs)

    def get(self, request, *args, **kwargs):
        '''Call each sections's get() view before rendering final response'''
        page = self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        sections = page.sections.all()
        for section in sections:
            view = section.__class__.view_class()
            view.get(request, section)
        context.update({
            'page': page,
            'sections': sections,
        })
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        '''Call the post() function of the correct section view'''
        try:
            pk = int(self.request.POST.get('section'))
        except:
            return HttpResponseBadRequest()

        page = self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        sections = page.sections.all()
        for section in sections:
            view = section.__class__.view_class()
            if section.pk == pk:
                result = view.post(request, section)
                if isinstance(result, HttpResponseRedirect):
                    return result
            else:
                view.get(request, section)
        context.update({
            'page': page,
            'sections': sections,
        })
        return self.render_to_response(context)

# The following views all require a logged-in staff member

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class TypeMixin(MenuMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields_per_type = {}
        for model, _ in Section.TYPES:
            ctype = ContentType.objects.get(
                app_label=Section._meta.app_label,
                model=model.lower(),
            )
            fields_per_type[ctype.model] = ctype.model_class().fields

        context.update({
            'fields_per_type': json.dumps(fields_per_type),
        })
        return context

class BaseUpdateView(generic.UpdateView):
    template_name = 'cms/edit.html'

    def form_valid(self, form):
        form.save()
        return redirect(self.request.session.get('previous_url'))

class UpdatePage(StaffRequiredMixin, MenuMixin, BaseUpdateView):
    model = Page
    form_class = PageForm

class UpdateSection(StaffRequiredMixin, TypeMixin, BaseUpdateView):
    model = Section
    form_class = SectionForm

class CreatePage(StaffRequiredMixin, MenuMixin, generic.CreateView):
    model = Page
    form_class = PageForm
    template_name = 'cms/new.html'

class CreateSection(StaffRequiredMixin, TypeMixin, generic.CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'cms/new.html'

    def form_valid(self, form):
        form.instance.page = Page.objects.get(pk=self.kwargs.get('pk'))
        form.save()
        return redirect(self.request.session.get('previous_url'))
