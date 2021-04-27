from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """
    A class used to handle the form when a new user register the website
    ...
    Attributes
    ----------
    email : str
        The string of the email of the user's input
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EditProfileForm(forms.ModelForm):
    """
    A class used to handle the form when a user need to edit their profile
    ...
    Attributes
    ----------
    email : str
        The string of the email of the user's input
    """
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ['profile_picture']

class CreateProfileForm(forms.ModelForm):
    """
    A class used to handle the form when a user create their profile
    ...
    """
    class Meta:
        model = Profile
        fields = ['profile_picture']