from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm, \
    AuthenticationForm


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "用户名"
        self.fields['email'].widget.attrs['placeholder'] = "邮箱"
        self.fields['password1'].widget.attrs['placeholder'] = "密码"
        self.fields['password2'].widget.attrs['placeholder'] = "确认密码"


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['nickname', 'link', 'avatar']


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "用户名"
        self.fields['password'].widget.attrs['placeholder'] = "密码"
