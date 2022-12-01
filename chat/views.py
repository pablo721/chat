import datetime
from itertools import chain
import re

from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.db.models import Q
from .forms import FindUsersForm, AddToChat, CreateChatForm, ClearChatForm
from .utils import see_users, clear_chat, clear_users_history
from .models import Message, Chat
from website.models import Account


class MessengerView(TemplateView):
    template_name = 'chat/messenger.html'
    find_users_form = FindUsersForm
    create_chat_form = CreateChatForm


    def post(self, request, *args, **kwargs):
        account = equest.user.user_account
        if 'add_friend' in str(request.POST):
            friend = Account.objects.get(id=request.POST['add_friend'])
            if friend not in account.friends.all():
                account.friends.add(friend)
                account.save()
                return HttpResponseRedirect(reverse('chat:chat', args=(friend.id,)))
        return HttpResponseRedirect(reverse('chat:messenger'))

    def get_context_data(self, *args, **kwargs):
        account = self.request.user.user_account
        user_id = account.id
        users_online = see_users()
        friends = [(f.user.username, f.id, f.user in users_online) for f in account.friends.all()]
        friend = None
        chats = None

        owned_chats = Chat.objects.filter(owner=account)
        joined_chats = account.users_chats.all()
        public_chats = Chat.objects.filter(private=False)

        search_results = []
        if 'name' in str(self.request.GET):
            find_form = FindUsersForm(self.request.GET)
            if find_form.is_valid():
                form_data = find_form.cleaned_data
                search_results = User.objects.filter(username__icontains=form_data['name'])
            else:
                print(f'Errors: {find_form.errors}')
        return {'user_id': user_id, 'friend': friend, 'friends': friends, 'chats': chats,
                 'online_users': users_online,
                'create_chat': self.create_chat_form, 'find_friends_form': self.find_users_form,
                'search_results': search_results, 'chat_id': 0, 'owned_chats': owned_chats, 'joined_chats':
                joined_chats, 'public_chats': public_chats}


class ChatView(MessengerView):
    template_name = 'chat/chat.html'

    def get(self, request, *args, **kwargs):
        print('gettin')
        print(kwargs)
        account = self.request.user.user_account
        chat_id = kwargs['chat_id']
        if not Chat.objects.filter(id=chat_id).exists():
            return HttpResponse('Forbidden. Chat does not exist..')
        chat = Chat.objects.get(id=chat_id)
        if chat.private and account not in chat.users.all():
            return HttpResponse('Forbidden. Need invite to join chat.')
        context = self.get_context_data(*args, **kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        account = self.request.user.user_account
        #friend = Account.objects.get(id=kwargs['friend_id'])
        if 'clear_history' in str(request.POST):
            print('clearing hist')
            print(kwargs)
            chat_id = kwargs['chat_id']
            if Chat.objects.filter(id=chat_id).exists():
                Message.objects.filter(chat_id=chat_id).delete()
                return HttpResponseRedirect(reverse('chat:chat', args=(chat_id,)))
            #clear_history(account.id, friend.id)


        elif re.search('leave_chat', str(request.POST)):
            print('leavin')
            print(request.POST)
            chat_id = request.POST['drop_from_chat_chat_id']
            if Chat.objects.filter(id=chat_id).exists():
                chat = Chat.objects.get(id=chat_id)

                if account == chat.owner:
                    chat.delete()
                elif account in chat.users.all():
                    Message.objects.create(sender=account, chat=chat, timestamp=datetime.datetime.now(),
                                                       content=f'{account} has left the chat.')

                    chat.users.remove(account)

                return HttpResponseRedirect(reverse('chat:messenger'))

        elif re.search('kick_from_chat', str(request.POST)):
            print('kickin')
            print(request.POST)
            chat_id = request.POST['drop_from_chat_chat_id']
            friend_id = request.POST['kick_from_chat']

            if not Account.objects.filter(id=friend_id).exists() or not Chat.objects.filter(id=chat_id).exists():
                return HttpResponse('No such chat or user.')
            friend = Account.objects.get(id=friend_id)
            chat = Chat.objects.get(id=chat_id)

            if chat.owner != account:
                return HttpResponse('Unauthorized. Only chat owner can kick users.')

            if friend == request.user.user_account:
                print('deletin')
                chat.delete()
                return HttpResponseRedirect(reverse('chat:messenger'))
            if friend in chat.users.all():
                chat.users.remove(friend)
                chat.save()
                return HttpResponseRedirect(reverse('chat:chat', args=(chat_id,)))

    def get_context_data(self, *args, **kwargs):
        account = self.request.user.user_account
        context = super().get_context_data(**kwargs)
        print(kwargs)
        chat_id = kwargs['chat_id']

        if 'chat_id' in kwargs.keys():
            chat, created = Chat.objects.get_or_create(id=kwargs['chat_id'], defaults={'owner': account,
                                                                                       'creation_date': datetime.datetime.now()})
            print(chat.users)
            print(chat.users.all())
            if account not in chat.users.all():
                chat.users.add(account)



        context['chat'] = chat
        context['chat_id'] = chat.id

        #context['unread_msgs'] = self.get_unread_msgs()

        context['messages'] = Message.objects.filter(chat=chat)
        context['account'] = account
        context['friend'] = friend if 'friend_id' in kwargs.keys() else None
        context['add_to_chat_form'] = AddToChat
        return context


def unread_messages(request):
    print('get unread')
    res = []
    for chat in request.user.user_account.users_chats.all():
        msgs = Message.objects.filter(chat=chat).filter(seen=False).values()
        for msg in msgs:
            msg['sender'] = Account.objects.get(id=msg['sender_id']).user.username
            res.append(msg)
    print(f' unread: {res}')
    return JsonResponse(res, safe=False)

def clear_expired(request):
    print('clearings')
    for msg in Message.objects.all():
        if msg.destruct_timer and (msg.timestamp.timestamp() + msg.destruct_timer) - datetime.datetime.now().timestamp() <= 0:
            msg.delete()
    return HttpResponse('deleted')


def send(request):
    if request.method == 'POST':
        print(f'send {request.POST}')
        chat_id = request.POST['chat']
        account = request.user.user_account
        print(account)
        date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=1)))
        destruct_timer = request.POST['destruct_timer']

        # expiry_date = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp() + int(destruct_timer)*1000)

        Message.objects.create(sender=account, chat_id=chat_id, content=request.POST['content'],
                               timestamp=date, destruct_timer=destruct_timer, sent=True)

        return HttpResponseRedirect(reverse('chat:chat', args=(chat_id,)))


def confirm_seen(request, chat_id):
    if request.method == 'POST':
        print(f'confirm seen: post {request.POST}')

        Message.objects.filter(chat_id=chat_id).filter(~Q(sender=request.user.user_account)).update(
            seen=True)  # .order_by('-timestamp')
    return HttpResponse('Messages have been seen.')


def confirm_delivery(request, chat_id):
    if request.method == 'POST':
        print(f'confirm deliv: req post {request.POST}')
        account = request.user.user_account
        Message.objects.filter(chat_id=chat_id).filter(~Q(sender=account)).update(
            delivered=True)  # .order_by('-timestamp')
        return HttpResponse('Delivery confirmed.')


def start_chat(request, friend_id):
    acc = request.user.user_account
    friend_acc = Account.objects.get(id=friend_id)
    for chat in acc.users_chats.all():
        if friend_acc in chat.users.all() and chat.users.all().count() < 3:
            print('gogogog')
            return HttpResponseRedirect(reverse('chat:chat', args=(chat.id,)))
    chat = Chat.objects.create(owner=acc, creation_date=datetime.datetime.now())
    Message.objects.create(sender=acc, chat=chat, timestamp=datetime.datetime.now(),
                           content=f'Chat created by {acc}')
    chat.users.add(acc)
    chat.users.add(friend_acc)
    return HttpResponseRedirect(reverse('chat:chat', args=(chat.id,)))










def delete_friend(request):
    account = request.user.user_account
    if request.method == "POST" and 'del_friend_btn' in str(request.POST):
        friend = Account.objects.get(id=request.POST['del_friend_btn'])
        if friend in account.friends.all():
            account.friends.remove(friend)
            account.save()
        return HttpResponseRedirect(reverse('chat:messenger'))


def add_to_chat(request):
    if request.method == 'POST':
        print(request.POST)
        user = request.user.user_account
        friend_id = request.POST['add_to_chat_btn']
        chat_id = request.POST['chat_id']
        if Account.objects.filter(id=friend_id).exists() and Chat.objects.filter(id=chat_id).exists():
            chat = Chat.objects.get(id=chat_id)
            if user != chat.owner:
                return HttpResponse('Forbidden. User is not owner of the chat.')
            friend = Account.objects.get(id=friend_id)
            chat.users.add(friend)
            chat.save()
            return HttpResponseRedirect(reverse('chat:chat', args=(chat.id,)))

def add_friend(request):
    if request.method == "POST" and 'add_friend' in str(request.POST):
        account = request.user.user_account
        friend = Account.objects.get(id=request.POST['add_friend'])
        if friend not in account.friends.all():
            account.friends.add(friend)
            account.save()
        if 'chat_id' in str(request.POST):
            if request.POST['chat_id']:
                return HttpResponseRedirect(reverse('chat:chat', args=(request.POST['chat_id'],)))
        return HttpResponseRedirect(reverse('chat:messenger'))


# class RoomView(MessengerView):
# 	model = Chat
# 	create_chats_form = CreateRoomForm
# 	template_name = 'chat/chats.html'
#
# 	def get_context_data(self, chat_id, *args, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		chat = Chat.objects.get(id=chat_id)
# 		context['chat'] = chat
# 		context['messages'] = Message.objects.filter(chat=chat)
# 		return context
#
# 	def post(self, request, *args, **kwargs):
# 		context = self.get_context_data(**kwargs)
# 		if 'join_chats_btn' in str(request.POST):
# 			chats = Chat.objects.get(id=request.POST['join_chats_btn'])
# 			account = request.user.user_account
# 			account.chats.add(chats)
# 			account.save()
# 		return HttpResponseRedirect(reverse('chat:chats', args=(context['chats'].id,)))
#
#
def create_chat(request):
    if request.method == "POST":
        chats_form = CreateRoomForm(request.POST)
        if chats_form.is_valid():
            form_data = chats_form.cleaned_data
            form_data['owner'] = request.user.user_account
            form_data['creation_date'] = datetime.datetime.now(datetime.timezone.utc)
            chats = Chat.objects.create(**form_data)
            return HttpResponseRedirect(reverse('chat:chat', args=(chats.id,)))
        else:
            print(f'errors: {chats_form.errors}')
            return HttpResponseRedirect(reverse('chat:chat', args=()))
