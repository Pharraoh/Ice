# from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
# from .views import UserProfileView

app_name = "feed"

urlpatterns = [
    path('feed/', views.feed, name = 'feed'),
    path('prof/', views.prof, name = 'prof'),
    # path('user/profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    # url('user/profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    # url('dashboard/', views.Dashboard.as_view(), name='dashboard'),
]

# path('settings/<int:pk>', views.AccountSettings.as_view(), name='edit-profile')
