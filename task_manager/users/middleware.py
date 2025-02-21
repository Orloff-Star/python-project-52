from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _

class PermissionDeniedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            messages.error(request, _("You do not have permission to change another user."))
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Редирект на предыдущую страницу
        return None