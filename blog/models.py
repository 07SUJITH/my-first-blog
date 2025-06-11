from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        """
        Returns a queryset of approved comments for this post.
        usage:
        approved_comments = post.approved_comments()
        This method filters the comments related to this post where 'approved_comment' is True.
        It allows you to easily access only the comments that have been approved for display.
        Returns:
            QuerySet: A queryset of Comment objects that are approved for this post.
        post.approved_comments.count # Returns the number of approved comments for this post.
        """
        return self.comments.filter(approved_comment=True).order_by('-created_date')

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    """
    Comment made by a user on a blog post.

    Fields:
        post (ForeignKey): related Post (cascade delete). The 'related_name="comments"'
            allows reverse lookup from a Post instance using 'post.comments.all()'.
        author (ForeignKey): comment author (nullable, set to NULL on user deletion).
        text (TextField): comment content.
        created_date (DateTimeField): creation timestamp.
        approved_comment (BooleanField): approval status.
      Methods:
        approve():
            Marks the comment as approved and saves the change to the database.

        __str__():
            Returns a readable string representation of the comment, including the author's name
            (or 'Anonymous' if missing) and a preview of the comment text (first 50 characters).
 
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.TextField(validators=[MaxLengthValidator(500)])
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        """Mark the comment as approved."""
        self.approved_comment = True
        self.save()

    def __str__(self):
        author_name = self.author.username if self.author else "Anonymous"
        return f"{author_name} - {self.text[:50]}{'...' if len(self.text) > 50 else ''}"