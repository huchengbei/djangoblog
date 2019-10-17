from django.urls import path

from oauth import views

app_name = 'oauth'
urlpatterns = [
    path(r'callback', views.callback, name='callback'),
]