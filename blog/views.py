import datetime

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from blog.models import Article, BlogSetting


class BaseArticlesListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'
    page_kwarg = 'page'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paginate_by = BlogSetting.get_settings().paginate_by

    def get_queryset(self):
        articles = super(BaseArticlesListView, self).get_queryset()
        now = datetime.datetime.now()
        return articles.filter(type='article', status='published', pub_time__lte=now)


class IndexView(BaseArticlesListView):
    pass


class CategoryArticlesView(BaseArticlesListView):

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        articles = super(CategoryArticlesView, self).get_queryset()
        return articles.filter(category__slug=slug)


class TagArticlesView(BaseArticlesListView):

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        articles = super(TagArticlesView, self).get_queryset()
        return articles.filter(tags__slug=slug)


class ArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super(ArticleView, self).get_object()
        obj.viewed()
        return obj
#     TODO: add judge when the article is draft or deleted @chengbei


class ArchiveView(BaseArticlesListView):
    template_name = 'blog/archives.html'
    context_object_name = 'archives'

    def get_queryset(self):

        class ArticleList(list):
            year = 0000
            month = 0
            day = 0
            type = ''

            def __init__(self, type='all', year=0000, month=0):
                super().__init__()
                self.type = type
                self.year = year
                self.month = month

            def __str__(self):
                if self.type == 'year':
                    return str(self.year)
                if self.type == 'month':
                    return str(self.month)
                if self.type == 'day':
                    return str(self.day)
                return 'NoName'

        articles = super(ArchiveView, self).get_queryset()
        old_year = 0000
        old_month = 0
        archives = ArticleList()
        year_list = ArticleList(type='year')
        month_list = ArticleList(type='month')
        for article in articles:
            year = article.pub_time.year
            month = article.pub_time.month
            if year != old_year:
                old_year = year
                if month_list:
                    year_list.append(month_list)
                month_list = ArticleList(type='month', month=month)
                if year_list:
                    archives.append(year_list)
                year_list = ArticleList(type='year', year=year)
            if month != old_month:
                old_month = month
                if month_list:
                    year_list.append(month_list)
                month_list = ArticleList(type='month', month=month)
            month_list.append(article)
        if month_list:
            year_list.append(month_list)
        if year_list:
            archives.append(year_list)

        return archives
