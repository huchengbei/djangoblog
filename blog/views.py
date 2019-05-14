from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from blog.models import Article


class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'


class ArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
