from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from account.forms import UserCreationForm, UserChangeForm
from account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ('username', 'nickname', 'email', 'link', 'is_staff', 'link_to_avatar', 'last_login', 'date_joined')
    list_display_links = ('username',)
    ordering = ['-id']

    def link_to_avatar(self, obj):
        link = obj.avatar
        return format_html(r'<a href="%s"><img style="width:50px;height:50px;" src="%s"></img></a>' % (link, link))
    link_to_avatar.short_description = '头像'

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.add_fieldsets += (
            (None, {
                'classes': ('wide',),
                'fields': ('email', ),
            }),
        )
        self.fieldsets += (
            (None, {'fields': ('avatar', )}),
        )
