from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, CreateView

from .models import Page
from .forms import PageForm, SectionForm
from .utils import get_config

import swapper
Section = swapper.load_model('cms', 'Section')

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class MenuMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = Page.objects.filter(menu=True)
        footer = get_config(10)
        context.update({
            'page_url_pattern': settings.PAGE_URL_PATTERN,
            'pages': pages,
            'footer': footer,
        })
        return context

class MemoryMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.session['previous_url'] = request.path
        return super().dispatch(request, *args, **kwargs)

class BasePageView(MenuMixin, MemoryMixin, DetailView):
    model = Page
    template_name = 'cms/page.html'

    def setup(self, request, *args, slug='', **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.kwargs['slug'] = slug

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.object
        sections = page.sections.all()
        context.update({
            'page': page,
            'sections': sections,
        })
        return context

class PageView(BasePageView):
    pass

class CreatePage(StaffRequiredMixin, MenuMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'cms/new.html'

class CreateSection(StaffRequiredMixin, MenuMixin, CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'cms/new.html'

    def form_valid(self, form):
        form.instance.page = Page.objects.get(pk=self.kwargs.get('pk'))
        form.save()
        return redirect(self.request.session.get('previous_url'))

class BaseUpdateView(StaffRequiredMixin, MenuMixin, UpdateView):
    template_name = 'cms/edit.html'

    def form_valid(self, form):
        form.save()
        return redirect(self.request.session.get('previous_url'))

class UpdatePage(BaseUpdateView):
    model = Page
    form_class = PageForm

class UpdateSection(BaseUpdateView):
    model = Section
    form_class = SectionForm
