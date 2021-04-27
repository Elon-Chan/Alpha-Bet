import sys
sys.path.append("..")

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse, redirect

# Create your models here.
class Profile(models.Model):
    """
    A class used to define the model of a profile
    ...
    Attributes
    ----------
    user : object
        the object of a user
    profile_picture : image
        the icon of a user
    
    Methods
    ----------
    get_absolute_url(self)
        get and return the url of the profile
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='img/profile/Alphabet_Icon.png', null=True, upload_to = 'img/profile/')

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('profile_edit_page', kwargs={'pk': self.pk})