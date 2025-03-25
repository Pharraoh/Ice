from django.urls import path, include
from . import views

app_name = "community"

urlpatterns = [
    path('activity/', views.activity, name = 'activity'),
    path('members/', views.members, name = 'members'),

]
