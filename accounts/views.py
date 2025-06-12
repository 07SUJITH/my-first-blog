# Import login to authenticate and start a session for a user after signup
from django.contrib.auth import login
# Import UserCreationForm for handling user registration and password validation
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    """
    user registration using Django's built-in UserCreationForm.
    Automatically logs in the user after successful registration.
    """
    # Redirect already authenticated users to home page
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            # Log in the user automatically after successful registration
            login(request, user)
            # Redirect to home page after signup
            return redirect('blog:post_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})