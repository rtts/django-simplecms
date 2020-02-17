import json
import swapper

from django.views import generic
from django.shortcuts import redirect
from django.views.generic.edit import FormMixin
from django.contrib.admin.utils import NestedObjects
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from .decorators import register_view
from .forms import PageForm, SectionForm, SectionFormSet

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

class SectionFormView(FormMixin, SectionView):
    '''Generic section with associated form'''

    def post(self, request):
        '''Process form'''
        form = self.get_form()
        if form.is_valid():
            form.save(request)
            return redirect(self.get_success_url())
        return form

class SectionFormSetView(SectionView):
    '''Generic section with associated form'''

    formset_class = None

    def post(self, request):
        '''Process form'''
        formset = self.get_formset()
        if formset.is_valid():
            formset.save(request)
            return redirect(self.get_success_url())
        return formset

    def get_formset(self):
        # todo: handle initials!
        return self.formset_class()

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = self.get_formset()
        return super().get_context_data(**kwargs)

class MenuMixin:
    '''Add pages to template context'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = Page.objects.filter(menu=True)
        context.update({
            'pages': pages,
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

    def initialize_section(self, section):
        section.view = section.__class__.view_class()
        section.view.setup(self.request, section)
        section.context = section.view.get_context_data(
            request = self.request,
            section = section,
        )

    def get(self, request, *args, **kwargs):
        '''Initialize sections and render final response'''
        page = self.object = self.get_object()
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

# The following views require a logged-in staff member

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class TypeMixin(MenuMixin):
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

class BaseUpdateView(generic.UpdateView):
    template_name = 'cms/edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'label_suffix': ''})
        return kwargs

    def form_valid(self, form):
        if 'delete' in self.request.POST:
            collector = NestedObjects(using='default')
            collector.collect([self.object])
            self.template_name = 'cms/confirm.html'
            return self.render_to_response(self.get_context_data(
                deleted = collector.nested(),
                protected = collector.protected,
                object = self.object,
            ))
        else:
            form.save()
        return redirect(self.request.session.get('previous_url'))

class UpdatePage(StaffRequiredMixin, TypeMixin, BaseUpdateView):
    model = Page
    form_class = PageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in context:
            context['formset'] = SectionFormSet(instance=self.object, form_kwargs={'label_suffix': ''})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = SectionFormSet(request.POST, request.FILES, instance=self.object)
        if form.is_valid() and formset.is_valid():
            formset.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

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
