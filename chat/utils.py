from online_users.models import OnlineUserActivity
import datetime
from django.contrib.auth.models import User
from .models import Message, Chat


def see_users():
    user_status = OnlineUserActivity.get_user_activities(time_delta=datetime.timedelta(seconds=60))
    return [user.user for user in user_status]


def drop_chat(user, chat_id):
    if Chat.objects.filter(id=chat_id).exists():
        chat = Chat.objects.get(id=chat_id)
        if user == chat.owner:
            chat.delete()
        else:
            print(f'Only owner can drop chat.')
    else:
        print(f'There is no room {chat_id}')


def clear_room(user, chat_id):
    if Chat.objects.filter(id=chat_id).exists():
        chat = Chat.objects.get(id=chat_id)
        if user == chat.owner:
            Message.objects.filter(chat_id=chat.id).delete()
        else:
            print(f'Only owner can clear chat.')
    else:
        print(f'There is no room {chat_id}')


# if all_msgs == True, deletes also received messages
# if all_msgs == False, only clears own messages
def clear_chat(user_id, friend_id, all_msgs=False):
    Message.objects.filter(sender=user_id).filter(recipient_id=friend_id).delete()
    if all:
        Message.objects.filter(sender=friend_id).filter(recipient_id=user_id).delete()


def clear_users_history(user_id):
    Message.objects.filter(sender=user_id).delete()
    Message.objects.filter(recipient_id=user_id).delete()


def format_timer(n_seconds, hours=True, minutes=True, seconds=True):
    res = ''
    if hours and n_seconds > 3600:
        hours = seconds // 3600
        n_seconds -= 3600 * hours
        res += f'{hours}h '
    if minutes and n_seconds > 60:
        minutes = n_seconds // 60
        n_seconds -= 60 * minutes
        res += f'{minutes}m '
    if seconds:
        res += f'{n_seconds}s'
    return res
