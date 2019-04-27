from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, CreateView

from .models import Page
from .forms import PageForm, SectionFormSet
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

class CreatePage(StaffRequiredMixin, MenuMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'cms/new.html'

class UpdatePage(StaffRequiredMixin, MenuMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'cms/edit.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = SectionFormSet(request.POST, request.FILES, instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form.save()
        formset.save()
        return redirect(form.instance.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in context:
            formset = SectionFormSet(instance=self.object)
            context.update({
                'formset': formset,
            })
        return context
