from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  


#class LogoutView(LogoutView):
#    next_page = reverse_lazy('login')

def logout_view(request):
    logout(request)  # Выход из аккаунта
    return redirect(reverse('home'))  # Перенаправление на страницу входа