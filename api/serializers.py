import datetime

from rest_framework import serializers
from chat.models import Message, Chat
#from spybot.models import Keyword, Watchlist, FlaggedMessage
from website.models import Account, Ban
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ['sender', 'chat', 'content', 'timestamp', 'sent', 'delivered',
				   'seen', 'destruct_timer']
	# sender = serializers.StringRelatedField()
	# chat = serializers.StringRelatedField()
	# content = serializers.StringRelatedField()
	# timestamp = serializers.DateTimeField(default=datetime.datetime.now())


class MessageReadSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ['sender', 'chat', 'content', 'timestamp', 'sent', 'delivered',
				   'seen', 'destruct_timer', 'remaining']

	sender = serializers.StringRelatedField()
	# def to_representation(self, instance):
	# 	response = super().to_representation(instance)
	# 	response['chat_messages'] = sorted(response['chat_messages'], key=lambda x: x['timestamp'])
	# 	return response



class ChatSerializer(serializers.ModelSerializer):
	class Meta:
		model = Chat
		fields = ['owner', 'chat_name', 'creation_date', 'users', 'chat_messages']

	owner = serializers.StringRelatedField(required=False)
	#chat_name = serializers.StringRelatedField(required=False)
	users = serializers.StringRelatedField(many=True, required=False)
	chat_messages = MessageReadSerializer(many=True, required=False)
	creation_date = serializers.DateTimeField(required=False)

	def to_representation(self, instance):
		response = super().to_representation(instance)
		response['chat_messages'] = sorted(response['chat_messages'], key=lambda x: x['timestamp'])
		return response





class AccountSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()
	friends = serializers.StringRelatedField()

	class Meta:
		model = Account
		fields = ['user', 'friends']




