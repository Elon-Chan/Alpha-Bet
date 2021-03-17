from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import reverse, redirect
from autoslug import AutoSlugField

User = get_user_model()
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='title')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('stockfloor_postdetail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('stockfloor_postupdate', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('stockfloor_postdelete', kwargs={'slug': self.slug})

class Tag(models.Model):
    name = models.CharField(max_length=150)
    #slug = models.SlugField(max_length=150, unique=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date_added = models.DateTimeField(default=timezone.now)
    #slug = models.SlugField(max_length=150)

    def __str__(self):
        return self.comment_author.username