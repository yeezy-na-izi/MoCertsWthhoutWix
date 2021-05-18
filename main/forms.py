from django import forms
from .models import MyCertsUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Имя'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Фамилия'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Подтвердите пароль'})

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class MyCertUserForm(forms.ModelForm):
    class Meta:
        model = MyCertsUser
        fields = ('profile_photo',)
