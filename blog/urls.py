from django.urls import path
from . import views
from blog.dash_apps.finished_apps import simple_example, candlestick_example # not used but must be imported in order to work

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('dash/', views.dash, name='blog-dash'),
    path('candlestick/', views.candlestick, name='blog-dash')
]
