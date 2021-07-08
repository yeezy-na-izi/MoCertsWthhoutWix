from django import forms
from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = [
            'email',
            'first_name',
            'last_name',
            'photo',
            'password1',
            'password2',
        ]


class MyCertUserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('photo',)


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = Account
        fields = [
            'email',
            'password1',
        ]
