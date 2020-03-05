"""Определяет схемы URL для пользователей."""
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'users'

urlpatterns = [
    # Страница входа
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    # Страница выхода
    url(r'^logout/$', views.logout_view, name='logout'),
    # Страница регистрации
    url(r'^register/$', views.register, name='register'),
]
