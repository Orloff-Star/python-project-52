from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from task_manager.tasks.models import Task
from .forms import TaskForm
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not authorized! Please log in."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'tasks_detail'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not authorized! Please log in."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Автор — текущий пользователь
        messages.success(self.request, _("The task has been created successfully."))
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not authorized! Please log in."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('task_list')
    success_message = _("Task changed successfully.")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not authorized! Please log in."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)
    

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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

    '''def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.task_set.exists():  # Проверка, связан ли статус с задачами
            messages.error(request, _("Cannot delete task because it is in use"))
            return redirect('task_list')
        return super().post(request, *args, **kwargs)'''