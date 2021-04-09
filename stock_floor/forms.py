from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tgtags',]

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control','placeholder':'Type your comment here!', 'rows':'7', 'cols':'30'})
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

print(UserCreationForm())

        