from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect


class OwnerRequiredMixin(UserPassesTestMixin):
    permission_denied_message = _(
        "You do not have permission to modify another user."
        )
    permission_denied_redirect = None

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        redirect_url = (self.permission_denied_redirect
                        or self.request.META.get('HTTP_REFERER', '/')
                        )
        return redirect(redirect_url)
