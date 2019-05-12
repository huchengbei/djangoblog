from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm, \
    AuthenticationForm


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['nickname', 'link', 'avatar']


class LoginForm(AuthenticationForm):
    pass
