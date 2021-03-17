from django.urls import path
from .views import (
    post_list,about,
    mainpage,
    tag_detail,
    tag_list,
    PostCreateView,
    TagCreate,
    PostUpdateView,
    PostDeleteView,
    PostCommentCreateView,
    PostDetailView
)
from . import views

urlpatterns = [
    path('', mainpage, name='stockfloor_blog'),
    path('stockfloor/about/', about, name='stockfloor_about'),
    path('stockfloor/', post_list, name='stockfloor_postlist'),
    path('stockfloor/post/<str:slug>/', PostDetailView.as_view(), name='stockfloor_postdetail'),
    path('stockfloor/post/<str:slug>/update/', PostUpdateView.as_view(), name='stockfloor_postupdate'),
    path('stockfloor/post/<str:slug>/delete/', PostDeleteView.as_view(), name='stockfloor_postdelete'),
    path('stockfloor/post/<str:slug>/comment/', PostCommentCreateView.as_view(), name='stockfloor_postcomment'),
    path('stockfloor/tag/<str:slug>/', tag_detail, name='tag_detail'),
    path('stockfloor/tags/', tag_list, name='tag_list'),
    path('stockfloor/create/post/', PostCreateView.as_view(template_name='stock_floor/post_create_form.html'), name='create'),
    path('stockfloor/create/tag/', TagCreate.as_view(), name='tag_create'),
]