from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse, redirect

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, null=True, upload_to = 'img/profile/')

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('profile_edit_page', kwargs={'pk': self.pk})