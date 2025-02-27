from django.urls import reverse_lazy
from task_manager.views import CheckAuthorizationViev
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.statuses.models import Status
from .forms import StatusForm
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from .forms import StatusForm


class StatusListView(CheckAuthorizationViev, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(CheckAuthorizationViev, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('status_list')
    success_message = _("The status has been created successfully.")


class StatusUpdateView(CheckAuthorizationViev, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('status_list')
    success_message = _("Status changed successfully.")


class StatusDeleteView(CheckAuthorizationViev, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('status_list')
    success_message = _("The status was successfully deleted.")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.task_set.exists():  # Проверка, связан ли статус с задачами
            messages.error(request, _("Cannot delete status because it is in use"))
            return redirect('status_list')
        return super().post(request, *args, **kwargs)
