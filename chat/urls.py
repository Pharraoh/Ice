from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path('chat/<str:username>/', views.one_on_one_chat, name='one_on_one_chat'),
    path('chats/', views.chat_list, name='chat_list'),
    path('send_message/<str:username>/', views.send_message, name='send_message'),
    # path('send-message/<int:room_id>/', views.send_message, name='send_message'),
    path('fetch_messages/<str:username>/', views.fetch_messages, name='fetch_messages'),
    # path('fetch-messages/<int:room_id>/', views.fetch_messages, name='fetch_messages'),
    path("post_status/", views.post_status, name='post_status'),
    path("fetch_statuses/", views.fetch_statuses, name='fetch_statuses'),

]
# 
