from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'password']
    success_url = reverse_lazy('login')

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'password']
    success_url = reverse_lazy('user_list')

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

class LoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class LogoutView(LogoutView):
    next_page = reverse_lazy('login')