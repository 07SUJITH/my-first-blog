from django import forms 
from .models import Post, Comment

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
        
class CommentForm(forms.ModelForm):
    '''
    Form for creating and updating comments on blog posts.
    '''
    class Meta:
        '''
        Meta class to define the model and fields for the form.
        Helps django to automatically generate form fields based on the model.
        '''
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'text': 'Comment',
        }
        help_texts = {
            'text': 'Enter your comment here.',
        }
        error_messages = {
            'text': {
                'required': 'This field is required.',
                'max_length': 'Comment is too long. Maximum 500 characters allowed.',
            },
        }