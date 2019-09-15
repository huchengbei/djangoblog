from django.urls import path

from comment import views

app_name = 'comment'
urlpatterns = [
    path(r'comment/post_comment', views.PostCommentView.as_view(), name='post_comment'),
]