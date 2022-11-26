import re
from chat.models import Chat, Message
from chat.models import Room
from website.models import Profile, Ban
from .models import Keyword, Watchlist, InterceptedMessage


def scan_users_history(user, keyword):
	pass


def scan_chat_history(chat, keyword):
	if sent:
		sent_msgs = Message.objects.filter(sender=user).filter(content__icontains=keyword)
	if received:
		rcvd_msgs = Message.objects.filter(sender=user).filter(content__icontains=keyword)

	return {'sent': sent_msgs, 'received': rcvd_msgs}



def scan_room_history(room, keyword):
	msgs = Message.objects.filter(room=room).filter(content__icontains=keyword)
	return msgs



def real_time_scan(keywords, chat, room, user, target):
	if target == 'u':
		msgs = None


def ban_user(user, reason, duration):
	pass



