import datetime
from itertools import chain
import re

from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .forms import FindUsersForm, InviteToRoom, CreateRoomForm, ClearChatForm
from .utils import see_users, clear_room, clear_chat, clear_users_history
from .models import Message, Room
from website.models import Profile


class MessengerView(TemplateView):
	template_name = 'chat/messenger.html'
	find_users_form = FindUsersForm
	create_room_form = CreateRoomForm

	def post(self, request, *args, **kwargs):
		profile = equest.user.user_profile
		if 'add_friend' in str(request.POST):
			friend = Profile.objects.get(id=request.POST['add_friend'])
			if friend not in profile.friends.all():
				profile.friends.add(friend)
				profile.save()
				return HttpResponseRedirect(reverse('chat:chat', args=(friend.id,)))
		return HttpResponseRedirect(reverse('chat:messenger'))

	def get_context_data(self, *args, **kwargs):
		profile = self.request.user.user_profile
		user_id = profile.id
		users_online = see_users()
		friends = [(f.user.username, f.id, f.user in users_online) for f in profile.friends.all()]
		friend = None
		room = None
		owned_rooms = Room.objects.filter(creator=profile)
		priv_rooms = profile.rooms.all()
		pub_rooms = Room.objects.filter(private=False)
		rooms = owned_rooms.union(priv_rooms, pub_rooms)

		search_results = []
		if 'name' in str(self.request.GET):
			find_form = FindUsersForm(self.request.GET)
			if find_form.is_valid():
				form_data = find_form.cleaned_data
				search_results = User.objects.filter(username__icontains=form_data['name'])
			else:
				print(f'Errors: {find_form.errors}')
		return {'user_id': user_id, 'friend': friend, 'friends': friends, 'pub_rooms': pub_rooms, 'rooms': rooms,
				'priv_rooms': priv_rooms, 'owned_rooms': owned_rooms, 'room': room, 'online_users': users_online,
				'create_room_form': self.create_room_form, 'find_friends_form': self.find_users_form,
				'search_results': search_results}


def send(request):
	if request.method == 'POST':
		print(f'send {request.POST}')
		profile = request.user.user_profile
		date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=1)))
		destruct_timer = request.POST['destr_timer']
		if re.search('friend_id', str(request.POST)):
			friend_id = request.POST['friend_id']
			Message.objects.create(sender=profile, recipient_id=friend_id, content=request.POST['msg_text'],
								   timestamp=date, destruct_timer=destruct_timer, sent=True)
			return HttpResponseRedirect(reverse('chat:chat', args=(friend_id,)))

		elif re.search('room_id', str(request.POST)):
			room_id = request.POST['room_id']
			Message.objects.create(sender=profile, room_id=room_id, content=request.POST['msg_text'],
								   timestamp=date, destruct_timer=destruct_timer, sent=True)
			return HttpResponseRedirect(reverse('chat:room', args=(room_id)))


def confirm_seen(request, friend_id):
	if request.method == 'POST':
		profile_id = request.user.user_profile.id
		print(f'confirm seen: post {request.POST}')
		msgs = Message.objects.filter(sender=friend_id).filter(recipient_id=profile_id)
		if msgs:
			for msg in msgs:
				msg.seen = True
				msg.save()
			return HttpResponse('Messages have been seen.')
		else:
			return HttpResponse('No messages')


def confirm_delivery(request, friend_id):
	if request.method == 'POST':
		print(f'confirm dev: req post {request.POST}')
		profile = request.user.user_profile
		friend = Profile.objects.get(id=friend_id)
		msgs = Message.objects.filter(sender=friend_id).filter(recipient_id=profile.id)
		for msg in msgs:
			msg.delivered = True
			msg.save()
		return HttpResponse('Delivery confirmed.')


class ChatView(MessengerView):
	template_name = 'chat/chat.html'

	def post(self, request, *args, **kwargs):
		profile = self.request.user.user_profile
		friend = Profile.objects.get(id=kwargs['friend_id'])
		if 'clear_history' in str(request.POST):
			clear_history(profile.id, friend.id)

	def get_context_data(self, *args, **kwargs):
		profile = self.request.user.user_profile
		context = super().get_context_data(**kwargs)
		friend = Profile.objects.get(id=kwargs['friend_id'])
		context['profile'] = profile
		context['friend'] = friend
		return context


def delete_friend(request):
	profile = request.user.user_profile
	if request.method == "POST" and 'del_friend_btn' in str(request.POST):
		friend = Profile.objects.get(id=request.POST['del_friend_btn'])
		if friend in profile.friends.all():
			profile.friends.remove(friend)
			profile.save()
		return HttpResponseRedirect(reverse('chat:messenger'))


def add_friend(request):
	if request.method == "POST" and 'add_friend' in str(request.POST):
		profile = request.user.user_profile
		friend = Profile.objects.get(id=request.POST['add_friend'])
		if friend not in profile.friends.all():
			profile.friends.add(friend)
			profile.save()
		return HttpResponseRedirect(reverse('chat:chat', args=(friend.id,)))


class RoomView(MessengerView):
	model = Room
	create_room_form = CreateRoomForm
	template_name = 'chat/room.html'

	def get_context_data(self, room_id, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		room = Room.objects.get(id=room_id)
		context['room'] = room
		context['messages'] = Message.objects.filter(room_id=room_id)
		return context

	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		if 'join_room_btn' in str(request.POST):
			room = Room.objects.get(id=request.POST['join_room_btn'])
			profile = request.user.user_profile
			profile.rooms.add(room)
			profile.save()
		return HttpResponseRedirect(reverse('chat:room', args=(context['room'].id,)))


def create_room(request):
	if request.method == "POST":
		room_form = CreateRoomForm(request.POST)
		if room_form.is_valid():
			form_data = room_form.cleaned_data
			form_data['creator'] = request.user.user_profile
			form_data['creation_date'] = datetime.datetime.now(datetime.timezone.utc)
			room = Room.objects.create(**form_data)
			return HttpResponseRedirect(reverse('chat:room', args=(room.id,)))
		else:
			print(f'errors: {room_form.errors}')
			return HttpResponseRedirect(reverse('chat:room', args=()))
