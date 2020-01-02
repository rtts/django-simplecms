import json

from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import PageForm, SectionForm
from .utils import get_config

import swapper
Page = swapper.load_model('cms', 'Page')
Section = swapper.load_model('cms', 'Section')

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class MenuMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = Page.objects.filter(menu=True)
        footer = get_config(10)
        context.update({
            'pages': pages,
            'footer': footer,
        })
        return context

class TypeMixin(MenuMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields_per_type = {}
        for model, desc in Section.TYPES:
            ctype = ContentType.objects.get(
                app_label=Section._meta.app_label,
                model=model.lower(),
            )
            fields_per_type[ctype.model] = ctype.model_class().fields

        context.update({
            'fields_per_type': json.dumps(fields_per_type),
        })
        return context

class MemoryMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.session['previous_url'] = request.path
        return super().dispatch(request, *args, **kwargs)

class PageView(MenuMixin, MemoryMixin, generic.DetailView):
    model = Page
    template_name = 'cms/page.html'

    # Supplies a default argument for slug
    def setup(self, *args, slug='', **kwargs):
        super().setup(*args, slug=slug, **kwargs)
        #self.request = request
        #self.args = args
        #self.kwargs = kwargs
        #self.kwargs['slug'] = slug

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.object
        sections = page.sections.all()
        context.update({
            'page': page,
            'sections': sections,
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
