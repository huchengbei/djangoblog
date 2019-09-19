from django import template

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.simple_tag(name='get_article_comment_list')
def get_article_comment_list(article_id, parent=None):
    comment_list = Comment.objects.filter(article_id=article_id, parent=parent)
    return comment_list


@register.simple_tag(name='get_comment_form')
def get_comment_form(article):
    form = CommentForm()
    form.fields['article'].initial = article
    return form


@register.simple_tag(name='get_comment_count')
def get_comment_count(article):
    return Comment.objects.filter(article=article).count()

