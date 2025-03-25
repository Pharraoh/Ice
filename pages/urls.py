from django.urls import path, include
from . import views

app_name = "pages"

urlpatterns = [
    path('about/', views.about, name = 'about'),
    path('membership/', views.membership, name = 'membership'),

]
