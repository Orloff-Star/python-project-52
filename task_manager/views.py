from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import HttpResponse
from task_manager.form import CustomAuthenticationForm
import logging


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(AuthLoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Добавляем сообщение об успешном входе
        messages.success(
            self.request,
            _('You are logged in')
        )
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
#        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, _("You are logged out"))
        return redirect(reverse('home'))


class CheckAuthorizationViev(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _("You are not authorized! Please log in.")
            )
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


logger = logging.getLogger(__name__)


def test_error(request):
    try:
        # Генерируем ошибку
        1 / 0
    except Exception as e:
        # Логируем ошибку
        logger.error(str(e), exc_info=True)
        return HttpResponse(
            "Произошла ошибка, но она была залогирована в Rollbar."
        )
