from django import forms 
from .models import Post

class PostForm(forms.ModelForm):
    '''
    Form for creating and updating blog posts.
    '''
    class Meta:
        '''
        Meta class to define the model and fields for the form.
        Helps django to automatically generate form fields based on the model.
        '''
        model = Post
        fields = ['title', 'text']
        
        