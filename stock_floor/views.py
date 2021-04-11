from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from .models import Post, Comment
from .forms import PostCreateForm, CommentCreateForm
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, CreateView, UpdateView, ListView
from hitcount.views import HitCountDetailView
from django.contrib import messages
from taggit.models import TagBase, Tag
from django.db.models import Q
from django.core.paginator import Paginator

def mainpage(request):
    return render(request, 'stock_floor/index.html', {'title': 'Welcome to Alpha Bet'})

@login_required
def post_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 6)

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
        
    context = {
        'page':page,
        'next_url':next_url,
        'prev_url':prev_url,
    }
    ordering = ['-date_posted']
    return render(request, 'stock_floor/post.html', context)

class PostDetailView(HitCountDetailView, ListView):
    model = Post
    template_name = 'stock_floor/post_detail.html'
    slug_field = "slug"
    object_list = Post.objects.all()

    form = CommentCreateForm

    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            form.instance.comment_author_id = self.request.user.id
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()

            return redirect(reverse('stockfloor_postdetail', kwargs={'slug': post.slug}))

    def get_context_data(self, **kwargs):
        comment = Comment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form':self.form,
            'comment': comment,
        })
        return context

    @login_required
    def post_detail(request, slug):
        post = Post.objects.get(slug__iexact=slug)
        return render(request, 'stock_floor/post_detail.html', context={'post': post,})

@login_required
def TgtagDetailList(request, slug):
        tgtag = Post.objects.filter(tgtags__name__in=[slug])
        tagname = slug

        paginator = Paginator(tgtag, 6)
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
            
        context = {
            'page':page,
            'next_url':next_url,
            'prev_url':prev_url,
            'tgtag':tgtag,
            'tagname':tagname,
        }

        return render(request, 'stock_floor/tgtag_detail.html', context)

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'tgtags', 'coverimg']

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
        bound_form = PostCreateForm(request.POST, request.FILES, instance=post)

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