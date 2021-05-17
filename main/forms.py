from django import forms
from .models import MyCertsUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class MyCertUserForm(forms.ModelForm):
    class Meta:
        model = MyCertsUser
        fields = ('profile_photo',)
