from django.urls import path
from . import views

app_name = 'realtime_chat'

# urlpatterns = [
#     path('', views.matched_users_view, name='matched_users'),
#     path('<str:username>/', views.chat_view, name='chat_room'),
#
#     path("post_status/", views.post_status, name='post_status'),
#     path("fetch_statuses/", views.fetch_statuses, name='fetch_statuses'),
#     path('delete_status/<uuid:status_id>/', views.delete_status, name='delete_status'),
#
#     path('<str:username>/mark-read/', views.mark_chat_read, name='mark_chat_read'),
# ]
urlpatterns = [
    path('', views.matched_users_view, name='matched_users'),

    path('check-unread-messages/', views.unread_count_view, name='check_unread_messages'),

    # ✅ Put specific patterns BEFORE generic ones
    path('<str:username>/mark-read/', views.mark_chat_read, name='mark_chat_read'),

    path("post_status/", views.post_status, name='post_status'),
    path("fetch_statuses/", views.fetch_statuses, name='fetch_statuses'),
    path('delete_status/<uuid:status_id>/', views.delete_status, name='delete_status'),

    # ✅ Generic pattern goes last
    path('<str:username>/', views.chat_view, name='chat_room'),

]
