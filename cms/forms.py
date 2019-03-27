from django import forms
from .models import Page, Section

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'

SectionFormSet = forms.inlineformset_factory(Page, Section, exclude='__all__', extra=0)
