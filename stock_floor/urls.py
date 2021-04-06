from django.urls import path
from .views import (
    post_list,about,
    mainpage,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostDetailView,
    TgtagDetailList,
    TgtaglList,
)
from . import views

urlpatterns = [
    path('', mainpage, name='stockfloor_blog'),
    path('stockfloor/about/', about, name='stockfloor_about'),
    path('stockfloor/', post_list, name='stockfloor_postlist'),
    path('stockfloor/post/<str:slug>/', PostDetailView.as_view(), name='stockfloor_postdetail'),
    path('stockfloor/tgtags/', TgtaglList, name='stockfloor_tgtagslist'),
    path('stockfloor/tgtags/<str:slug>', TgtagDetailList, name='stockfloor_tgtagsdetail'),
    path('stockfloor/post/<str:slug>/update/', PostUpdateView.as_view(), name='stockfloor_postupdate'),
    path('stockfloor/post/<str:slug>/delete/', PostDeleteView.as_view(), name='stockfloor_postdelete'),
    path('stockfloor/create/post/', PostCreateView.as_view(template_name='stock_floor/post_create_form.html'), name='create'),
]