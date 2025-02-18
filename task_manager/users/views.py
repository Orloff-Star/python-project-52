from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import RegisterForm, UserUpdateForm, PasswordChangeForm


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

'''class UserCreateView(CreateView):
    model = User
    template_name = 'users/user_create.html'
    fields = ['username', 'password']
    success_url = reverse_lazy('login')'''


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect("home")  # Перенаправление на главную страницу
    else:
        form = RegisterForm()
    return render(request, "users/user_register.html", {"form": form})


'''class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_update.html'
    fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
    success_url = reverse_lazy('user_list')'''

#@login_required
def update(request, pk):
    instance = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Обновляем сессию, чтобы не разлогинивать пользователя
            return redirect('user_list')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'users/user_update.html', {
        'user_form': user_form,
        'password_form': password_form,
    })


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')

