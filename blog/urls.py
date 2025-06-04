from django.urls import path
from . import views


# Assigns a URL namespace to this app so you can reverse namespaced URLs (e.g. 'blog:post_list') without collisions.
app_name = 'blog' # Namespace for the blog app

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('about/', views.about, name='about'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]