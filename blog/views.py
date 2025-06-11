from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from django.core.paginator import Paginator
from django.conf import settings
from .forms import PostForm, CommentForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages

# Create your views here.

def post_list(request):
    """
    Retrieve published blog posts, paginate them, and render the post list template.
    """
    # Creates a lazy QuerySet 
    posts_qs = (
        Post.objects
            .select_related('author')
            .filter(published_date__lte=timezone.now())
            .order_by('-published_date')
    )

    # Slices the QuerySet into pages (still lazy)
    paginator = Paginator(posts_qs, getattr(settings, "POSTS_PER_PAGE", 5))
    # Gets the page number from the request, defaults to 1
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page) 
    # Template receives already-fetched data
    return render(request, 'blog/post_list.html', {'page_obj': posts})

def post_detail(request, pk):
    """
    Display a single blog post.
    """
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def about(request):
    """
    Render the about page.
    """
    return render(request, 'blog/about.html')

@login_required
def post_new(request):
    '''
    Create a new blog post.
    login_required decorator is used in post_new view function to ensure that only authenticated users can create new blog posts.if the user is not logged in, they will be redirected to the login page.
    '''
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})



@login_required
def post_edit(request, pk):
    '''
    Edit an existing blog post.
    login_required decorator is used in post_edit view function to ensure that only authenticated users can edit existing blog posts.if the user is not logged in, they will be redirected to the login page.
    '''
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied("You do not have permission to edit this post.")
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    """
    Retrieve draft blog posts, paginate them, and render the post list template.
    login_required decorator ensures that only authenticated users can access this view.
    """
    # Creates a lazy QuerySet 
    posts_qs = (
        Post.objects
            .select_related('author')
            .filter(published_date__isnull=True)
            .order_by('-created_date')
    )

    # Slices the QuerySet into pages (still lazy)
    paginator = Paginator(posts_qs, getattr(settings, "POSTS_PER_PAGE", 5))
    # Gets the page number from the request, defaults to 1
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page) 
    # Template receives already-fetched data
    return render(request, 'blog/post_draft_list.html', {'page_obj': posts})

@login_required
def post_publish(request, pk):
    """
    Publish a draft blog post.
    login_required decorator ensures that only authenticated users can access this view.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # Only allow publishing via POST requests to prevent unintended access via URL.
        # This avoids republishing drafts or altering the publish date by direct GET access.    
        post.publish()
    return redirect('blog:post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    """
    Remove a blog post.
    login_required decorator ensures that only authenticated users can access this view.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # Only allow removal via POST requests to prevent unintended access via URL.
        post.delete()
    return redirect('blog:post_list') 


@login_required
def add_comment_to_post(request, pk):
    """
    Add a comment to a blog post.
    Handles both GET and POST requests - GET shows the post with form, POST processes the comment.
    """
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        is_post_author = (post.author == request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            # Automatically set approved_comment to True if the author is the current user
            comment.approved_comment = True if is_post_author else False
            comment.save()
            
            # Add success message
            if is_post_author:
                messages.success(request, 'Your comment has been submitted.')
            else:
                # If the comment is not from the author, it will be pending approval
                messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('blog:post_detail', pk=post.pk)
        else:
            # If form is invalid, show the post detail page with form errors
            messages.error(request, 'Please correct the errors in your comment.')
            return render(request, 'blog/post_detail.html', {
                'post': post,
                'comment_form': form,
                'show_modal': True  # Flag to show modal with errors
            })
    else:
        # For GET requests, just redirect to post detail
        return redirect('blog:post_detail', pk=post.pk)


@login_required
def comment_approve(request, pk):
    """
    Approve a comment on a blog post.
    login_required decorator ensures that only authenticated users can approve comments.
    Raises PermissionDenied if the user is not the author of the post.
    """
    
    comment = get_object_or_404(Comment, pk=pk)
    if comment.post.author != request.user:
        raise PermissionDenied
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    """
    Remove a comment from a blog post.
    login_required decorator ensures that only authenticated users can remove comments.
    Raises PermissionDenied if the user is not the author of the post.
    """
    
    comment = get_object_or_404(Comment, pk=pk)
    # Only the comment author or the post author can remove the comment
    if comment.author != request.user and comment.post.author != request.user:
        raise PermissionDenied
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)