from django import forms
from .models import Label
from django.utils.translation import gettext as _


class LabelForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput())

    class Meta:
        model = Label
        fields = ['name']
