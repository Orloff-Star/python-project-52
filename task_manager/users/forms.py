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


class UpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('old_password', None)