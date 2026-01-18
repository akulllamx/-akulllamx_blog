from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Главная с последними постами
    path('', views.home, name='home'),

    # Список всех постов
    path('posts/', views.post_list, name='post_list'),

    # Один пост
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]

