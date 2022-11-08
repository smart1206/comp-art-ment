from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('art_gallery/', views.art_gallery, name='index'),
    path('global_art/', views.global_art, name='global_index'),
    path('global_art/<int:art_id>/', views.global_art_detail, name='global_detail'),
    path('art/<int:art_id>/', views.art_detail, name='detail'),
    path('art/create/', views.ArtCreate.as_view(), name='art_create'),
    path('art/<int:pk>/update/', views.ArtUpdate.as_view(), name='art_update'),
    path('art/<int:pk>/delete/', views.ArtDelete.as_view(), name='art_delete'),
    path('profile/create/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profile/<int:pk>/update', views.ProfileUpdate.as_view(), name='profile_update'),
    # path('collection', views.collection, name='collection'),
    path('accounts/signup/', views.signup, name='signup'),
    path('art/<int:art_id>/add_art_photo/', views.add_art_photo, name='add_art_photo'),
    path('art/<int:profile_id>/add_profile_photo/', views.add_profile_photo, name='add_profile_photo'),
]