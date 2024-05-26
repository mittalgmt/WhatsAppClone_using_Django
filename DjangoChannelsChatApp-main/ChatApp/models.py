from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# User = get_user_model()


class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name
    
    def return_room_messages(self):

        return Message.objects.filter(room=self)
    
    def create_new_room_message(self, sender, message):

        new_message = Message(room=self, sender=sender, message=message)
        new_message.save()

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return str(self.room)

class ChatType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# privatechat
class PrivateChat(models.Model):
    me = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='it_me')
    frnd = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='my_frnd')
    chats = models.JSONField(default=dict)

# file sharing
class filesharing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file_field = models.FileField(upload_to='uploads/')
    desc = models.TextField()

    def __str__(self):
        return f'{self.user}=> {self.title}'