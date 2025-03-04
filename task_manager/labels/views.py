from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.labels.models import Label
from .forms import LabelForm
from django.utils.translation import gettext as _
from django.contrib import messages
from task_manager.views import CheckAuthorizationViev
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin


class LabelListView(CheckAuthorizationViev, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(CheckAuthorizationViev, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('label_list')
    success_message = _("The label has been created successfully.")


class LabelUpdateView(CheckAuthorizationViev, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('label_list')
    success_message = _("Label changed successfully.")


class LabelDeleteView(CheckAuthorizationViev, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('label_list')
    success_message = _("The label was successfully deleted.")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.labels.exists():
            messages.error(
                request, _("Cannot delete label because it is in use")
            )
            return redirect('label_list')
        return super().post(request, *args, **kwargs)
