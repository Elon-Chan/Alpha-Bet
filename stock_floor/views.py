from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from .models import Post, Tag, Comment
from .forms import PostCreateForm, TagCreateForm, CommentCreateForm
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, CreateView, UpdateView
from django.contrib import messages

def mainpage(request):
    return render(request, 'stock_floor/mainpage.html', {'title': 'Welcome to Alpha Bet'})

def about(request):
    return render(request, 'stock_floor/about.html', {'title': 'About Alpha Bet'})

@login_required
def post_list(request):
    post = Post.objects.order_by('-date_posted')
    context = {
        'post':post,
    }
    return render(request, 'stock_floor/post.html', context)

@login_required
def post_detail(request, slug):
    post = Post.objects.get(slug__iexact=slug)
    return render(request, 'stock_floor/post_detail.html', context={'post': post,})

@login_required
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'stock_floor/tag_list.html', context={'tags':tags})

def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    return render(request, 'stock_floor/tag_detail.html', context={'tag':tag})

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post

    def get(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = PostCreateForm(instance=post)
        return render(request, 'stock_floor/post_update.html', context={'form':bound_form, 'post':post})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug__iexact=slug)
        bound_form = PostCreateForm(request.POST, instance=post)

        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        
        return render(request, 'stock_floor/post_update.html', context={'form':bound_form, 'post':post})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        return render(request, 'stock_floor/post_delete.html', context={'post':post})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug__iexact=slug)
        post.delete()
        
        return redirect('stockfloor_postlist')

class PostCommentCreateView(CreateView):
    model = Comment
    #form_class = CommentCreateForm
    template_name = 'stock_floor/post_add_comment.html'
    fields = '__all__'
    success_url = '/stockfloor'

class TagCreate(View):
    def get(self, request):
        form = TagCreateForm()
        return render(request, 'stock_floor/tag_create.html', context={'form':form})

    def post(self, request):
        bound_form = TagCreateForm(request.POST)

        if bound_form.is_valid():
            new_tag = bound_form.cleaned_data['name']
            if Tag.objects.filter(name=new_tag).count():
                messages.error(request, 'Tag has been created before.')
                return render(request, 'stock_floor/tag_create.html', context={'form':bound_form})
            new_tag = bound_form.save()
            return redirect(new_tag)
        
        return render(request, 'stock_floor/tag_create.html', context={'form':bound_form})