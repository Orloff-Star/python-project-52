from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import RegisterForm, UpdateForm
from django.utils.translation import gettext as _
from .forms import UpdateForm, UserPasswordChangeForm
from django.contrib import messages



class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserRegisterViev(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/user_register.html'
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Registration was successful! You can now log in.'))
        return response


class UserUpdateView(UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['password_form'] = UserPasswordChangeForm(user=self.request.user, data=self.request.POST)
        else:
            context['password_form'] = UserPasswordChangeForm(user=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        password_form = context['password_form']
        if password_form.is_valid():
            password_form.save()
        messages.success(self.request, _('User successfully changed'))
        return super().form_valid(form)
    

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('User deleted successfully'))
        return super().delete(request, *args, **kwargs)

