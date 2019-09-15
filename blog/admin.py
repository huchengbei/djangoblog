from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from blog.forms import NavigationForm
from blog.models import Article, Tag, Category, FriendLink, ExtendsSideBar, BlogSetting, Navigation, Link


def publish_article(modeladmin, request, queryset):
    queryset.update(status='published')


def draft_article(modeladmin, request, queryset):
    queryset.update(status='draft')


def open_article_comment_status(modeladmin, request, queryset):
    queryset.update(status='draft')


def close_article_comment_status(modeladmin, request, queryset):
    queryset.update(status='draft')


publish_article.short_description = '发布所选文章'
draft_article.short_description = '所选文章设为草稿'
open_article_comment_status.short_description = '开启所选文章评论功能'
close_article_comment_status.short_description = '关闭所选文章评论功能'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('body', 'title')
    # form = ArticleForm
    list_display = (
        'id', 'title', 'author', 'link_to_category', 'views', 'status', 'type', 'create_time', 'pub_time',
        'update_time')
    list_display_links = ('id', 'title')
    list_filter = ('author', 'status', 'type', 'category', 'tags')
    filter_horizontal = ('tags',)
    view_on_site = True
    actions = [publish_article, draft_article, open_article_comment_status, close_article_comment_status]

    @staticmethod
    def link_to_category(obj):
        url_pattern = 'admin:%s_%s_change' % (obj.category._meta.app_label, obj.category._meta.model_name)
        link = reverse(url_pattern, args=(obj.category.id,))
        return format_html(r'<a href="%s">%s</a>' % (link, obj.category.name))

    link_to_category.short_description = '分类目录'

    def get_view_on_site_url(self, obj=None):
        if obj:
            return obj.get_absolute_url()
        else:
            return BlogSetting.get_site_url()


@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):
    exclude = ['create_time', 'update_time']
    list_select_related = ['parent', ]
    form = NavigationForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ['create_time', 'update_time']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    exclude = ['create_time', 'update_time']


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    exclude = ['create_time', 'update_time']


@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    exclude = ['create_time', 'update_time']


@admin.register(ExtendsSideBar)
class ExtendsSideBarAdmin(admin.ModelAdmin):
    exclude = ['create_time', 'update_time']


@admin.register(BlogSetting)
class BlogSettingAdmin(admin.ModelAdmin):
    exclude = ['create_time', 'update_time']
