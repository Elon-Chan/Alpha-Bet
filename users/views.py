from django.shortcuts import render, redirect
from .forms import UserRegisterForm, EditProfileForm, CreateProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Profile
from stock_floor.models import Post
from django.core.paginator import Paginator
import re
from django.utils.html import strip_tags

def textify(html):
    """Remove HTML tag
    Parameters
    ----------
    html : str
        The html string need to be read
    """
    text_only = re.sub('[ \t]+', ' ', strip_tags(html))
    return text_only.replace('\n ', '\n').strip()

UserModel = get_user_model()

def register(request):
    """Register function
    Parameters
    ----------
    request : object
        the request object need to be used in the framework
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('users/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, "users/activate_done.html")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {'form': form})

@login_required
def profile(request, pk):
    """User profile page view
    Parameters
    ----------
    request : object
        the request object need to be used in the framework
    pk : int
        the user id of a profile
    """
    posts = Post.objects.filter(author=pk)
    author = User.objects.get(id=pk)

    for post in posts:
        post.content = textify(post.content)
        post.content = post.content.replace("&nbsp;", ' ')
        post.content = post.content.replace("&#39;", '\'')

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    post = Post.objects.order_by('-date_posted')
    context = {
        'page':page,
        'next_url':next_url,
        'prev_url':prev_url,
        'posts':posts,
        'author':author,
    }
    return render(request, 'users/profile.html', context)

def activate_done(request):
    """Finish register new account page view (before email confirmation)
    """
    return render(request, "users/activate_done.html")

def activate_complete(request):
    """Finish activate new account page view
    """
    return render(request, "users/activate_complete.html")

def activate(request, uidb64, token):
    """A function used to handle new account's activation
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "users/activate_complete.html")
    else:
        return HttpResponse('Activation link is invalid!')

class EditProfilePageView(generic.UpdateView):
    """
    A class used to handle the edit of a user profile
    ...
    Attributes
    ----------
    model : object
        The model need to be used
    template_name : str
        HTML template need to be used for font end

    Methods
    ----------
    get_redirect_url(self, pk)
        get the redirect url
    """
    model = Profile
    template_name = 'users/profile_edit.html'
    # success_url = reverse_lazy('profile')
    fields = ['profile_picture']

    def get_redirect_url(self, pk):
        return reverse_lazy('profile',
                            kwargs={'pk': pk},)

class CreateProfileView(CreateView):
    """
    A class used to handle the edit of a user profile
    ...
    Attributes
    ----------
    model : object
        The model need to be used
    form_class : class
        the form need to be used for creating a profile
    template_name : str
        HTML template need to be used for font end

    Methods
    ----------
    form_valid(self, form)
        get the valid form from client
    """
    model = Profile
    form_class = CreateProfileForm
    template_name = 'users/profile_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)