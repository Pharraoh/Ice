from django.urls import path, include
from . import views

from .views import get_lgas

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),

    path('get-lgas/<int:state_id>/', get_lgas, name='get_lgas'),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('search/', views.user_search, name='user_search'),
    path('online-users/', views.online_users_view, name='online_users'),


    path('password-reset/', views.custom_password_reset, name='password_reset'),
    path('password-reset/done/', views.custom_password_reset_done, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
    path('password-reset-complete/', views.custom_password_reset_complete, name='password_reset_complete'),

]
