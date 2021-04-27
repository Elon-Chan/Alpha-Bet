from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostCreateForm(forms.ModelForm):
    """
    A class used to handle the creation form of a post
    ...
    Attributes
    ----------
    model : object
        The model need to be used
    fields : 
        the fields of the form when creating a post
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'tgtags', 'coverimg']

class CommentCreateForm(forms.ModelForm):
    """
    A class used to handle the creation form of a comment
    ...
    Attributes
    ----------
    model : object
        The model need to be used
    fields : 
        the fields of the form when creating a post
    """
    class Meta:
        model = Comment
        fields = ['comment']

        labels = {
            'comment': '',
        }

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control','placeholder':'Write your comment here!', 'rows':'7', 'cols':'30'})
        }

class UserRegisterForm(UserCreationForm):
    """
    A class used to handle the registation form of a user
    ...
    Attributes
    ----------
    email : str
        The string of the email of the user's input
    """
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
