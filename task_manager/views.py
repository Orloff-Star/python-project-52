from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib import messages
from django.utils.translation import gettext as _

class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(AuthLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Добавляем сообщение об успешном входе
        messages.success(self.request, _('You have successfully logged in!'))
        return super().form_valid(form)
    

'''def logout_view(request):
    logout(request)  # Выход из аккаунта
    return redirect(reverse('home'))  # Перенаправление на страницу входа'''

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
#        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, _("You have successfully logged out."))
        return redirect(reverse('home'))