from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from django.core.paginator import Paginator
from django.conf import settings
from .forms import PostForm

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
    post = Post.objects.filter(pk=pk).first()
    status = 404 if not post else 200
    return render(request, 'blog/post_detail.html', {'post': post}, status=status)

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