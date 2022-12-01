from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views



app_name = 'chat'
urlpatterns = [
    path(r'', login_required(views.MessengerView.as_view()), name='messenger'),
    path(r'<int:chat_id>', login_required(views.ChatView.as_view()), name='chat'),
    path(r'create_chat', login_required(views.create_chat), name='create_chat'),
    path(r'send', login_required(views.send), name='send'),
    path(r'start_chat/<int:friend_id>', views.start_chat, name='start_chat'),
    path(r'add_friend', login_required(views.add_friend), name='add_friend'),
    path(r'unread_messages/', login_required(views.unread_messages), name='unread_messages'),
    path(r'clear_expired/', login_required(views.clear_expired), name='clear_expired'),
    path(r'add_to_chat', login_required(views.add_to_chat), name='add_to_chat'),
    path(r'delete_friend', login_required(views.delete_friend), name='delete_friend'),
    path(r'confirm_delivery/<int:chat_id>', login_required(views.confirm_delivery), name='confirm_delivery'),
    path(r'confirm_seen/<int:chat_id>', login_required(views.confirm_seen), name='confirm_seen'),
    ]



