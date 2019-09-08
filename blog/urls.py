from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'article/<slug:slug>', views.ArticleView.as_view(), name='article'),
    path(r'page/<slug:slug>', views.ArticleView.as_view(), name='page'),
    path(r'category/<slug:slug>', views.IndexView.as_view(), name='category'),
    path(r'tag/<slug:slug>', views.IndexView.as_view(), name='tag'),
    path(r'archive', views.ArchiveView.as_view(), name='tag'),
]