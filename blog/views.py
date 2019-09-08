from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from blog.models import Article


class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        articles = super(IndexView, self).get_queryset()
        return articles.filter(type='article', status='published')


class CategoryArticlesView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        articles = super(CategoryArticlesView, self).get_queryset()
        return articles.filter(type='article', status='published').filter(category__slug=slug)


class TagArticlesView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        articles = super(TagArticlesView, self).get_queryset()
        return articles.filter(type='article', status='published').filter(tags__slug=slug)


class ArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super(ArticleView, self).get_object()
        obj.viewed()
        return obj
#     TODO: add judge when the article is draft or deleted @chengbei


class ArchiveView(ListView):
    model = Article
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

        articles = super(ArchiveView, self).get_queryset().order_by('pub_time')
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
                    year_list.insert(0, month_list)
                month_list = ArticleList(type='month', month=month)
                if year_list:
                    archives.insert(0, year_list)
                year_list = ArticleList(type='year', year=year)
            if month != old_month:
                old_month = month
                if month_list:
                    year_list.insert(0, month_list)
                month_list = ArticleList(type='month', month=month)
            month_list.insert(0, article)
        if month_list:
            year_list.insert(0, month_list)
        if year_list:
            archives.insert(0, year_list)

        return archives
