from django.contrib import admin

# Register your models here.
from comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('body', 'title')
    exclude = ['update_time']
    list_display = ('id', 'user',  'username', 'email', 'website', 'content', 'article', 'create_time')
    list_display_links = ('id', 'content')
