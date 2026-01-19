from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
]

