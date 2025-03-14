from django import forms
from .models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label=_("Status"))
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,        
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Executor'),
        to_field_name='id',
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False,
        label=_('Labels')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {'description': _('Description')}
