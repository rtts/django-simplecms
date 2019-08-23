from django import forms
from .models import Page, Section, SubSection

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        exclude = ['page']

class SubSectionForm(forms.ModelForm):
    class Meta:
        model = SubSection
        exclude = ['section']

SectionFormSet = forms.inlineformset_factory(Page, Section, exclude='__all__', extra=0)
SubSectionFormSet = forms.inlineformset_factory(Section, SubSection, exclude='__all__', extra=0)
