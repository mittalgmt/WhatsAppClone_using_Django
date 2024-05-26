import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ChatApp.models import *
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from time import sleep

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        event = {
            'type': 'send_message',
            'message': message,
        }

        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):

        data = event['message']
        await self.create_message(data=data)

        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):

        get_room_by_name = Room.objects.get(room_name=data['room_name'])
        
        if not Message.objects.filter(message=data['message']).exists():
            new_message = Message(room=get_room_by_name, sender=data['sender'], message=data['message'])
            new_message.save()  
        

# private chat
class PrivatechatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print(f"================== {self.scope['user']}")
        await self.accept() 
        await self.channel_layer.group_add(f"mychat_app_{self.scope['user']}", self.channel_name)
         
         
    async def disconnect(self, close_code): 
        pass
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data = json.loads(text_data)
        await self.channel_layer.group_send(
            f"mychat_app_{text_data['user']}",
            {
                'type':'send.msg',
                'msg':text_data['msg']
            }
            )
        await self.save_chat(text_data)

    @database_sync_to_async   
    def save_chat(self,text_data):
        frnd = User.objects.get(username=text_data['user'])
        mychats, created = PrivateChat.objects.get_or_create(me=self.scope['user'], frnd=frnd)
        # If the object was just created, initialize the 'chats' field as an empty dictionary
        if created:
            mychats.chats = {}
        mychats.chats[str(datetime.datetime.now())+"1"] = {'user': 'me', 'msg': text_data['msg']}
        mychats.save()
        mychats, created = PrivateChat.objects.get_or_create(me=frnd, frnd=self.scope['user'])
        # If the object was just created, initialize the 'chats' field as an empty dictionary
        if created:
            mychats.chats = {}
        mychats.chats[str(datetime.datetime.now())+"2"] = {'user': frnd.username, 'msg': text_data['msg']}
        mychats.save()
    async def send_videonofication(self,event):
        await  self.send(event['msg'])

    async def send_msg(self,event):
        print(event['msg'])
        await  self.send(event['msg'])
    async def chat_message(self, event):
        print(event['message'])
        await self.send(json.dumps("Total Online :- "+str(event['message'])))