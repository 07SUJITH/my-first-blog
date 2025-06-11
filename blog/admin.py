"""
admin.py

Register the Post model with Django’s admin site.

By registering Post here, you’ll be able to:
    - Create, read, update and delete blog posts
    - Manage posts via Django’s web-based admin interface at /admin/
"""

from django.contrib import admin
from .models import Post, Comment

# Register the Post model so it appears in /admin/
admin.site.register(Post)
# Register the Comment model so it appears in /admin/
admin.site.register(Comment)