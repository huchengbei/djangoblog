from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm

from account.models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['nickname']


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['nickname', 'link', 'avatar']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ('username', 'nickname', 'email', 'link', 'is_staff', 'avatar', 'last_login', 'date_joined')
    list_display_links = ('username',)
    ordering = ['-id']
