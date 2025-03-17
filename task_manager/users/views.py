from django.urls import reverse_lazy
from task_manager.views import CheckAuthorizationViev
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from .forms import RegisterForm, UpdateForm, UserPasswordChangeForm
from django.utils.translation import gettext as _
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateViev(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('User successfully registered')
        )
        return response


class UserUpdateView(CheckAuthorizationViev, UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied
        return obj

    '''def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['password_form'] = UserPasswordChangeForm(
                user=self.request.user,
                data=self.request.POST
            )
        else:
            context['password_form'] = UserPasswordChangeForm(
                user=self.request.user
            )
        return context'''

    def form_valid(self, form):
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        if password1 and password1 == password2:
            self.object.set_password(password1)
        messages.success(self.request, _('User successfully update'))
        return super().form_valid(form)


class UserDeleteView(CheckAuthorizationViev, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('User successfully deleted'))
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.authored_tasks.exists() or
                self.object.executor_tasks.exists()):
            messages.error(
                request,
                _("Cannot delete user because it is in use")
            )
            return redirect('user_list')
        return self.delete(request, *args, **kwargs)

