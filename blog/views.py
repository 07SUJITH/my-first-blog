from django.shortcuts import render, redirect, get_object_or_404
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
    post = Post.objects.filter(pk=pk, published_date__lte=timezone.now()).first()
    status = 404 if not post else 200
    return render(request, 'blog/post_detail.html', {'post': post}, status=status)

def about(request):
    """
    Render the about page.
    """
    return render(request, 'blog/about.html')

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.auther = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
