from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment
from autoslug import AutoSlugField


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