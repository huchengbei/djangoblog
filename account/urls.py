from django.urls import path

from account import views

app_name = 'account'
urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('change_profile', views.ChangeView.as_view(), name='change'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]