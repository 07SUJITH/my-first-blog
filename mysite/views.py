from django.shortcuts import render

def custom_permission_denied_view(request, exception):
    """
    Custom view to handle permission denied errors (HTTP 403).
    This view renders a custom 403 error page.
    """
    return render(request, 'errors/403.html', status=403)

def custom_page_not_found_view(request, exception):
    """
    Custom view to handle page not found errors (HTTP 404).
    This view renders a custom 404 error page.
    """
    return render(request, 'errors/404.html', status=404)

def custom_error_view(request):
    """
    Custom view to handle server errors (HTTP 500).
    This view renders a custom 500 error page.
    """
    return render(request, 'errors/500.html', status=500)