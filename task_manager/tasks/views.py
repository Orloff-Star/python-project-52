from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from task_manager.tasks.models import Task
from .forms import TaskForm
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from task_manager.views import CheckAuthorizationViev


class TaskListView(CheckAuthorizationViev, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status_id=status)

        executor = self.request.GET.get('executor')
        if executor:
            queryset = queryset.filter(executor_id=executor)

        label = self.request.GET.get('label')
        if label:
            queryset = queryset.filter(labels__id=label)

        self_tasks = self.request.GET.get('self_tasks')
        if self_tasks:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context


class TaskDetailView(CheckAuthorizationViev, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'tasks_detail'


class TaskCreateView(CheckAuthorizationViev, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request,
            _("The task has been created successfully.")
        )
        return super().form_valid(form)


class TaskUpdateView(CheckAuthorizationViev, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('task_list')
    success_message = _("Task changed successfully.")


class TaskDeleteView(CheckAuthorizationViev, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task_list')
    success_message = _("The task was successfully deleted.")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request, _("Only its author can delete a task."))
        return redirect('task_list')
