import markdown
from django import template
from django.template.defaultfilters import stringfilter

from blog.models import Article, Category, Tag

register = template.Library()

extension_configs = {
    'markdown.extensions.codehilite': {
        'linenums': True,
    },
}


def get_md():
    return markdown.Markdown(extensions=[
        # 'markdown.extensions.extra',
        'markdown.extensions.fenced_code',
        'markdown.extensions.footnotes',
        'markdown.extensions.tables',
        'markdown.extensions.codehilite',
        'markdown.extensions.meta',
        'markdown.extensions.toc'
    ], extension_configs=extension_configs
    )


@register.simple_tag(name='get_nav_dict')
def get_nav_dict():
    dic = {}
    from blog.models import Navigation
    parent_nav_list = Navigation.objects.filter(parent=None, is_show=True)
    for nav in parent_nav_list:
        dic[nav] = {}

    def make_dict(d):
        for key, value in d.items():
            sub_nav_list = Navigation.objects.filter(parent=key, is_show=True)
            if sub_nav_list:
                for nav in sub_nav_list:
                    d[key][nav] = {}
                make_dict(d[key])
            elif key.type == 'category':
                category_id = key.instance_id
                c = Category.objects.get(id=category_id)
                article_list = Article.objects.filter(category=c, type='article', status='published')
                for article in article_list:
                    d[key][article] = {}

    make_dict(dic)
    return dic


@register.simple_tag(name='markdown_to_html')
@register.filter(name='markdown_to_html')
@stringfilter
def markdown_to_html(body):
    md = get_md()
    return md.convert(body)


@register.simple_tag(name='get_article_list')
def get_article_list(sort=None, num=None):
    if sort:
        if num:
            return Article.objects.order_by(sort)[:num]
        return Article.objects.order_by(sort)
    if num:
        return Article.objects.all()[:num]
    return Article.objects.all()


@register.simple_tag(name='get_category_list')
def get_category_list():
    from django.db.models import Count
    from django.db.models import Q
    return Category.objects.annotate(article__count=Count('article', filter=Q(article__type='article')))


@register.simple_tag(name='get_tag_list')
def get_tag_list():
    from django.db.models import Count
    from django.db.models import Q
    # return Tag.objects.annotate(Count('article', filter=Q(article__type='article')))
    return Tag.objects.annotate(article__count=Count('article', filter=Q(article__type='article')))
