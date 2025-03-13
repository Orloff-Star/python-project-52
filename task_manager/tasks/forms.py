from django import forms
from .models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.utils.translation import gettext as _


class TaskForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label=_("Status"))
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False,
        label='Labels'
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
