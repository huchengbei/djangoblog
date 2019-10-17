from django.contrib import admin

# Register your models here.
from oauth.models import Platform, UserEx


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    exclude = ['create_time', 'update_time']


@admin.register(UserEx)
class UserExAdmin(admin.ModelAdmin):
    exclude = ['create_time', 'update_time']
