from django.shortcuts import render

# Create your views here.

def post_list(request):
    '''
    Function to render the post list page.
    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: Rendered HTML page for the post list.
    '''
    return render(request, 'blog/post_list.html', {})
