from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import reverse, redirect
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

User = get_user_model()

class Post(models.Model):
    """
    A class used to define the model of a post
    ...
    Attributes
    ----------
    title : str
        the title of the post
    content : str
        the content of a post
    date_posted : str
        the create date of the post
    author : str
        the author of a post
    slug : str
        the unique string of a post
    tgtags : TaggableManager object
        the tags of a post
    coverimg : image
        the cover image of a post
    
    Methods
    ----------
    get_absolute_url(self)
        get and return the url of the post
    get_update_url(self):
        get and return the post update url
    get_delete_url(self):
        get and return the delete post url
    get_tag_name(self):
        get and return the list of tags of the post
    """
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='title')
    tgtags = TaggableManager()
    coverimg = models.ImageField(blank=True, null=True, upload_to = 'img/')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('stockfloor_postdetail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('stockfloor_postupdate', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('stockfloor_postdelete', kwargs={'slug': self.slug})

    def get_tag_name(self):
        return self.tgtags.name
    class Meta:
        ordering = ['-date_posted']

class Comment(models.Model):
    """
    A class used to define the model of a post
    ...
    Attributes
    ----------
    post : object
        the object of a post
    comment_author : str
        the author of a comment
    comment : str
        the content of a comment
    comment_date_added : str
        the date of a comment
    parent : object
        the current post
    """
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date_added = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, related_name="replies", blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_author.username