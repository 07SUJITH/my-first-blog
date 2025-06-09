from django.urls import path
from django.contrib.auth import views as auth_views


# Assigns a URL namespace to this app so you can reverse namespaced URLs (e.g. 'accounts:login') without collisions.
app_name = 'accounts' # Namespace for the accounts app


urlpatterns = [
    # set template_name to the login.html file in the accounts/templates/accounts directory otherwise it will look at registration/login.html
    # This is the default template for the login view in Django, but you can customize it.
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # set next_page to '/' so that after logging out, the user is redirected to the home page
    # otherwise it will redirect to accounts/logout.html
    # This is the default template for the logout view in Django, but you can customize it.
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
