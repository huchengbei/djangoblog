from urllib.parse import quote

from django import template

from oauth.models import Platform

register = template.Library()


@register.simple_tag(name='get_oauth_app_list')
def get_oauth_app_list():
    platform_list = Platform.objects.filter(is_show=True)
    return platform_list


@register.simple_tag(name='get_redirect_url')
def get_redirect_url(callback_url, next, slug):
    if not next:
        from blog.models import BlogSetting
        next = BlogSetting.get_site_url()
    url = '{callback_url}?next={next}&slug={slug}'.format(callback_url=callback_url, next=quote(next), slug=slug)
    return quote(url)
