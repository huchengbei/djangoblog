from django.contrib import admin

# Register your models here.
from comment.models import Comment


def close_comment_status(modeladmin, request, queryset):
    queryset.update(status='close')


def open_comment_status(modeladmin, request, queryset):
    queryset.update(status='open')


close_comment_status.short_description = '屏蔽'
open_comment_status.short_description = '开放'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('body', 'title')
    exclude = ['update_time']
    list_display = ('id', 'user', 'username', 'email', 'website', 'content', 'article', 'create_time')
    list_display_links = ('id', 'content')

    readonly_fields = list_display + ('parent',)

    actions = [close_comment_status, open_comment_status]
