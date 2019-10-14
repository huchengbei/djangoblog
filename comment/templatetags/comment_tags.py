from django import template

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.simple_tag(name='get_article_comment_list')
def get_article_comment_list(article_id, parent=None):
    comment_list = Comment.objects.filter(article_id=article_id, parent=parent)
    return comment_list


@register.simple_tag(name='get_comment_form')
def get_comment_form(article, user, parent_id=None):
    form = CommentForm()
    form.fields['article'].widget.attrs['hidden'] = 'true'
    form.fields['article'].initial = article
    form.fields['parent'].widget.attrs['hidden'] = 'true'
    if parent_id:
        parent = Comment.objects.get(id=parent_id)
        form.fields['parent'].initial = parent
    if user.is_authenticated:
        form.fields['username'].widget.attrs['hidden'] = 'true'
        form.fields['username'].initial = user.nickname
        form.fields['email'].widget.attrs['hidden'] = 'true'
        form.fields['email'].initial = user.email
        form.fields['website'].widget.attrs['hidden'] = 'true'
        form.fields['website'].initial = user.link
    return form


@register.simple_tag(name='get_comment_count')
def get_comment_count(article):
    return Comment.objects.filter(article=article).count()

