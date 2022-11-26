import datetime
import re
from itertools import chain
from django.shortcuts import render
import django_filters.rest_framework as rest_filters
from rest_framework import viewsets, filters, generics
from django.contrib.auth.models import User
from django.http import JsonResponse
from .serializers import *
from chat.models import *
from .utils import delete_messages


class MonitorView(viewsets.ModelViewSet):
	queryset = Message.objects.all()
	serializer_class = MessageSerializer


class UsersView(viewsets.ModelViewSet):
	queryset = User.objects.all()


class RoomsView(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	filter_backends = [rest_filters.DjangoFilterBackend]

	def get_queryset(self):
		rooms = Room.objects.filter(private=False)


class MessagesView(viewsets.ModelViewSet):
	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	filter_backends = [rest_filters.DjangoFilterBackend]

	def get_queryset(self):
		profile = self.request.user.user_profile
		delete_messages(profile.id)

		if re.search('friend_id', str(self.request.GET)):
			friend_id = self.request.GET['friend_id']
			friend = Profile.objects.get(user=friend_id)
			sent_msgs = Message.objects.filter(sender=profile, recipient_id=friend_id).values()
			received_msgs = Message.objects.filter(sender=friend, recipient_id=profile.id).values()
			msgs = sent_msgs.union(received_msgs).order_by('timestamp')

		elif re.search('room_id', str(self.request.GET)):
			room_id = self.request.GET['room_id']
			msgs = Message.objects.filter(room_id=room_id).values().order_by('timestamp')
		else:
			return 'Friend id or room_id must be provided'

		for msg in msgs:
			msg['sender_id'] = Profile.objects.get(id=msg['sender_id']).user.username
			if msg['destruct_timer']:
				tz_info = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
				msg_date = msg['timestamp']
				now = datetime.datetime.now(tz=tz_info)
				delta = (now - msg_date).total_seconds()
				msg['destruct_timer'] = msg['destruct_timer'] - delta

		print(msgs)
		return msgs


