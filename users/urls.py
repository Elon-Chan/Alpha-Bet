from django.urls import path
from .views import profile, EditProfilePageView, CreateProfileView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<int:pk>/profile/', profile, name='profile'),
    path('<int:pk>/profile/profile_edit/', EditProfilePageView.as_view(), name='profile_edit_page'),
    path('new_profile_edit/', CreateProfileView.as_view(), name='new_profile_edit_page'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)