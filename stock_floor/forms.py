from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Tag, Comment
from autoslug import AutoSlugField


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags',]

class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
        }

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_author', 'comment_content']

        widgets = {
            'comment_author': forms.TextInput(attrs={'class': 'form-control'}),
            'comment_content': forms.Textarea(attrs={'class': 'form-control'})
        }