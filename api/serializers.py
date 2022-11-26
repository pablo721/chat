from rest_framework import serializers
from chat.models import Message, Room
from spybot.models import Keyword, Watchlist, FlaggedMessage
from website.models import Profile, Ban

from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ['id', 'sender_id', 'recipient_id', 'room_id', 'content', 'timestamp', 'sent', 'delivered',
				   'seen', 'destruct_timer']


class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = ['room_name', 'creator', 'users', 'private', 'creation_date']

