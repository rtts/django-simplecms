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

class PageView(MenuMixin, DetailView):
    model = Page
    template_name = 'cms/page.html'

class CreatePage(StaffRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'cms/new.html'

class CreateSection(StaffRequiredMixin, CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'cms/new.html'

    def form_valid(self, form):
        form.instance.page = Page.objects.get(pk=self.kwargs.get('pk'))
        form.save()
        return redirect(reverse('cms:updatepage', args=[form.instance.page.pk]))

class CreateSubSection(StaffRequiredMixin, CreateView):
    model = SubSection
    form_class = SubSectionForm
    template_name = 'cms/new.html'

    def form_valid(self, form):
        form.instance.section = Section.objects.get(pk=self.kwargs.get('pk'))
        form.save()
        return redirect(reverse('cms:updatesection', args=[form.instance.section.pk]))

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
        return redirect(self.get_absolute_url(form.instance))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in context:
            formset = self.formset_class(instance=self.object)
            context.update({
                'formset': formset,
                'formset_form_url': self.get_formset_form_url(self.object),
                'formset_description': self.formset_class.model._meta.verbose_name.title(),
            })
        return context

class UpdatePage(BaseUpdateView):
    model = Page
    form_class = PageForm
    formset_class = SectionFormSet

    def get_formset_form_url(self, page):
        return reverse('cms:createsection', args=[page.pk])

    def get_absolute_url(self, instance):
        return instance.get_absolute_url()

class UpdateSection(BaseUpdateView):
    model = Section
    form_class = SectionForm
    formset_class = SubSectionFormSet

    def get_formset_form_url(self, page):
        return reverse('cms:createsubsection', args=[page.pk])

    def get_absolute_url(self, instance):
        return instance.page.get_absolute_url()
