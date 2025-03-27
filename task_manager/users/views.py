from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from task_manager.views import CheckAuthorizationView
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import RegisterForm, UpdateForm
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .mixins import OwnerRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_login')
    success_message = _('User successfully registered')


class UserUpdateView(CheckAuthorizationView,
                     OwnerRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')
    success_message = _('User successfully updated')
    permission_denied_redirect = reverse_lazy('user_list')


class UserDeleteView(CheckAuthorizationView,
                     OwnerRequiredMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')
    success_message = _('User successfully deleted')
    permission_denied_redirect = reverse_lazy('user_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.authored_tasks.exists() or
                self.object.executor_tasks.exists()):
            messages.error(
                request,
                _('Cannot delete user because it is in use')
            )
            return redirect('user_list')
        return super().post(request, *args, **kwargs)
