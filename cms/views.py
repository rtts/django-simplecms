from django.views.generic import DetailView, UpdateView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import *
from .forms import *
from .utils import *

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

class EditPageMixin:
    model = Page
    form_class = PageForm
    template_name = 'cms/edit.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = SectionFormSet(request.POST, instance=self.object)
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

class UpdatePage(StaffRequiredMixin, MenuMixin, EditPageMixin, UpdateView):
    pass
class CreatePage(StaffRequiredMixin, MenuMixin, EditPageMixin, CreateView):
    def get_object(self):
        pass

class CreateSection:
    pass
