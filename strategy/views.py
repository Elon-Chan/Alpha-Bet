from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, "strategy/home.html")

def experimental(request):
    return render(request, "strategy/experimental.html")

def hedge(request):
    return render(request, "strategy/hedge.html")