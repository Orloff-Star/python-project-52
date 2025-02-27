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
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
#from task_manager.labels.models import Label


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not authorized! Please log in."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
#        Фильтрация задач на основе параметров запроса.
        queryset = super().get_queryset()

        # Фильтр по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status_id=status)

        # Фильтр по исполнителю
        executor = self.request.GET.get('executor')
        if executor:
            queryset = queryset.filter(executor_id=executor)

        # Фильтр по метке
#        label = self.request.GET.get('label')
 #       if label:
 #           queryset = queryset.filter(labels__id=label)

        # Фильтр по задачам текущего пользователя
        self_tasks = self.request.GET.get('self_tasks')
        if self_tasks:
            queryset = queryset.filter(author=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        #Добавляем в контекст данные для фильтров.
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()  # Все статусы для фильтра
        context['executors'] = User.objects.all()  # Все исполнители для фильтра
#        context['labels'] = Label.objects.all()  # Все метки для фильтра
        return context


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