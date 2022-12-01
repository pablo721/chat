import datetime
import re
from itertools import chain
from django.shortcuts import render, get_object_or_404

import django_filters.rest_framework as rest_filters
from rest_framework import viewsets, filters, generics, views
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.http import JsonResponse
from .serializers import *
from chat.models import *
from .utils import delete_expired_messages




class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all() #.order_by('-timestamp')

    serializer_class = MessageReadSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]



    def list(self, request, *args, **kwargs):
        #print(self.queryset)
        print('listin')

        serializer = MessageReadSerializer(self.queryset, many=True) #.order_by('timestamp')
        print(serializer.data)
        return Response(serializer.data)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     queryset = get_object_or_404(self.queryset, pk=pk)
    #     serializer = MessageSerializer(queryset)
    #     print(serializer.data)
    #     return Response(serializer.data)


# class RoomViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     filter_backends = [rest_filters.DjangoFilterBackend]


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]

    @action(detail=True, methods=['put'], name='Rename')
    def update_name(self, request, pk=None):
        chat = Chat.objects.get(pk=pk)
        serializer = ChatSerializer(request.data)
        #chat = Chat.objects.get(pk=pk)
        #print(data['chat_name'])
        new_name = serializer.__dict__['_args'][0]['chat_name']
        chat.chat_name = new_name
        chat.save()
        return Response()

    # def retrieve(self, request, pk, *args, **kwargs):
    #     queryset = get_object_or_404(self.queryset, pk=pk)
    #     messages = queryset.chat_messages.all().order_by('timestamp')
    #     serializer = ChatSerializer(queryset)
    #     serializer['chat_messages'] = MessageSerializer(messages)
    #     print(serializer.data)
    #     return Response(serializer.data)
