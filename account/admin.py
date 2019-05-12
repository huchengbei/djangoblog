from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.forms import UserCreationForm, UserChangeForm
from account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ('username', 'nickname', 'email', 'link', 'is_staff', 'avatar', 'last_login', 'date_joined')
    list_display_links = ('username',)
    ordering = ['-id']
