from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, CreateView

from .models import Page, Section, SubSection
from .forms import PageForm, SectionFormSet, SectionForm, SubSectionFormSet, SubSectionForm
from .utils import get_config

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class MenuMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = Page.objects.filter(menu=True)
        footer = get_config(10)
        context.update({
            'pages': pages,
            'footer': footer,
        })
        return context

class MemoryMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.session['previous_url'] = request.path
        return super().dispatch(request, *args, **kwargs)

class PageView(MenuMixin, MemoryMixin, DetailView):
    model = Page
    template_name = 'cms/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.object
        sections = page.sections.all()
        context.update({
            'page': page,
            'sections': sections,
        })
        return context

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

class CreateSubSection(StaffRequiredMixin, MenuMixin, CreateView):
    model = SubSection
    form_class = SubSectionForm
    template_name = 'cms/new.html'

    def form_valid(self, form):
        form.instance.section = Section.objects.get(pk=self.kwargs.get('pk'))
        form.save()
        return redirect(self.request.session.get('previous_url'))

class BaseUpdateView(StaffRequiredMixin, MenuMixin, UpdateView):
    template_name = 'cms/edit.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.formset_class(request.POST, request.FILES, instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form.save()
        formset.save()
        return redirect(self.request.session.get('previous_url'))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in context:
            formset = self.formset_class(instance=self.object)
            context.update({
                'formset': formset,
                'formset_form_url': self.get_formset_form_url(self.object),
                'formset_description': self.formset_class.model._meta.verbose_name,
            })
        return context

class UpdatePage(BaseUpdateView):
    model = Page
    form_class = PageForm
    formset_class = SectionFormSet

    def get_formset_form_url(self, page):
        return reverse('cms:createsection', args=[page.pk])

class UpdateSection(BaseUpdateView):
    model = Section
    form_class = SectionForm
    formset_class = SubSectionFormSet

    def get_formset_form_url(self, page):
        return reverse('cms:createsubsection', args=[page.pk])
