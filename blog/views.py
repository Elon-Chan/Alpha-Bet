from django.shortcuts import render
from .models import Post

# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def dash(request):
    return render(request, 'blog/dash.html')

def candlestick(request):
    return render(request, 'blog/candlestick.html')

