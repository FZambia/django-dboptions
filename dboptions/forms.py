# coding: utf-8
from django import forms
from dboptions.models import Option, to_final_value
from django.utils.translation import ugettext_lazy as _


class OptionForm(forms.ModelForm):

    class Meta:
        model = Option
        exclude = ()

    def clean(self):
        self.cleaned_data = super(OptionForm, self).clean()
        name = self.cleaned_data['name']
        value = self.cleaned_data['value']
        try:
            to_final_value(name, value)
        except ValueError:
            raise forms.ValidationError(_("malformed value for option"))
        return self.cleaned_data
