"""Определяет схемы URL для pixlands."""

from django.conf.urls import url

from . import views

app_name = 'pixlands'

urlpatterns = [
    # Домашняя страница
    url(r'^$', views.index, name='index'),
    # Вывод публичных тем
    url(r'^topics/$', views.topics, name='topics'),
    # Вывод личных тем
    url(r'^profile/$', views.profile, name='profile'),
    # Страница с подробной информацией по отдельной теме
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    # Страница для добавления новой темы
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    # Страница для добавления нового изображения
    url(r'^add_image/(?P<topic_id>\d+)/$', views.add_image, name='add_image'),
    # Страница для добавления изображения пользователя
    url(r'^add_profile_pic/$', views.add_profile_pic, name='add_profile_pic'),
    # Страница для редактирования темы
    url(r'^edit_topic/(?P<topic_id>\d+)/$', views.edit_topic, name='edit_topic'),
    # Страница редактирования текста изображения и удаления
    url(r'^edit_image/(?P<image_id>\d+)/$', views.edit_image, name='edit_image'),
    # Страница для удаления темы
    url(r'^delete_topic/(?P<topic_id>\d+)/$', views.delete_topic, name='delete_topic'),
    # Страница для удаления фото
    url(r'^delete_image/(?P<image_id>\d+)/$', views.delete_image, name='delete_image'),
    # Страница изображения
    url(r'^image/(?P<image_id>\d+)/$', views.image, name='image'),
    # Страница добавления комментария
    url(r'^add_comment/(?P<image_id>\d+)/$', views.add_comment, name='add_comment'),
    # Страница лайка на странице изображеия
    url(r'^like_on_image/(?P<image_id>\d+)/$', views.like_on_image, name='like_on_image'),
    # Страница лайка на странице топика
    url(r'^like_on_topic/(?P<image_id>\d+)/$', views.like_on_topic, name='like_on_topic'),
    # Страница лайка на странице поиска
    url(r'^like_on_search/(?P<image_id>\d+)/$', views.like_on_search, name='like_on_search'),
    # Страница для удаления комментария
    url(r'^delete_comment/(?P<comment_id>\d+)/$', views.delete_comment, name='delete_comment'),
    # Страница поиска
    url(r'^search/$', views.search, name='search'),
]