from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "用户名"
        self.fields['email'].widget.attrs['placeholder'] = "邮箱"
        self.fields['password1'].widget.attrs['placeholder'] = "密码"
        self.fields['password2'].widget.attrs['placeholder'] = "确认密码"


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'nickname', 'email', 'link', 'avatar']


class PasswordChangeForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.instance.set_password(password)
        return super().save(commit)


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "用户名"
        self.fields['password'].widget.attrs['placeholder'] = "密码"
