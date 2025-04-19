from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
# from .views import UserProfileView

app_name = "members"

urlpatterns = [
    path('allmembers/', views.allmembers, name = 'allmembers'),
    path('prof/', views.prof, name = 'prof'),
    path('feed/', views.feed, name = 'feed'),
    path('like/<str:username>/', views.like_user, name='like_user'),

    path('matches/', views.matched_users, name='matched_users'),
    path('search_members/', views.search_members, name='search_members'),
    # path('user/profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    # url('user/profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    # url('dashboard/', views.Dashboard.as_view(), name='dashboard'),
]
