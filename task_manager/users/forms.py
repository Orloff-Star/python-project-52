from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label=_('First name'), widget=forms.TextInput())
    last_name = forms.CharField(label=_('Last name'), widget=forms.TextInput())

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')