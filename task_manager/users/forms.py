from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


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
        label=_('New password'),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'required': 'required'
        }),
        required=True,
        strip=False,
        help_text=_('Enter your new password'),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'required': 'required'
        }),
        required=True,
        strip=False,
        help_text=_('To confirm, please enter your password again.'),
    )

    class Meta:
        model = get_user_model()
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password1',
                  'password2'
                  )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1:
            raise ValidationError(_("Password is required"))

        if password1 != password2:
            raise ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password1"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('old_password', None)
