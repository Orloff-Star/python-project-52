from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label=_('Name'),
                                 widget=forms.TextInput()
                                 )
    last_name = forms.CharField(label=_('Surname'),
                                widget=forms.TextInput()
                                )

    class Meta:
        model = get_user_model()
        fields = ['first_name',
                  'last_name',
                  'username',
                  'password1',
                  'password2'
                  ]


class UpdateForm(UserChangeForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password1',
                  'password2'
                  )


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('old_password', None)
