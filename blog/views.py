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


class ArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super(ArticleView, self).get_object()
        obj.viewed()
        return obj
#     TODO: add judge when the article is draft or deleted @chengbei
