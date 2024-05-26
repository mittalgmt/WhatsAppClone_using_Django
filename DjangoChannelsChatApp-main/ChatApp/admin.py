from django.contrib import admin
from .models import *

admin.site.register(Room)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender', 'message']

admin.site.register(Message, MessageAdmin)

admin.site.register(PrivateChat)

class PrivateChatAdmin(admin.ModelAdmin):
    list_display = ['id','me','frnd', 'chats']

@admin.register(filesharing)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'file_field']
