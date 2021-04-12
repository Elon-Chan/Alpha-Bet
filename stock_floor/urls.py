from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    post_list,
    mainpage,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostDetailView,
    TgtagDetailList,
)
from . import views

urlpatterns = [
    path('', mainpage, name='stockfloor_blog'),
    path('stockfloor/', post_list, name='stockfloor_postlist'),
    path('stockfloor/post/<str:slug>/', PostDetailView.as_view(), name='stockfloor_postdetail'),
    path('stockfloor/tgtags/<str:slug>', TgtagDetailList, name='stockfloor_tgtagsdetail'),
    path('stockfloor/post/<str:slug>/update/', PostUpdateView.as_view(), name='stockfloor_postupdate'),
    path('stockfloor/post/<str:slug>/delete/', PostDeleteView.as_view(), name='stockfloor_postdelete'),
    path('stockfloor/create/post/', PostCreateView.as_view(template_name='stock_floor/post_create_form.html'), name='create'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)