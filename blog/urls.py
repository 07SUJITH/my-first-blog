from django.urls import path
from . import views


# Assigns a URL namespace to this app so you can reverse namespaced URLs (e.g. 'blog:post_list') without collisions.
app_name = 'blog' # Namespace for the blog app

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('about/', views.about, name='about'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]