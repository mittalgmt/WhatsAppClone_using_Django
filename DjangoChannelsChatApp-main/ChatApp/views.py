from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# User = get_user_model()

# the main index fiel
def index(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'index.html', context={'users': users})

# login and signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user object to the database
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('login')  # Redirect to chat type selection page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    # Redirect authenticated users to the chat type selection page
    # if request.user.is_authenticated:
    #     return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('chat_type')  # Redirect to chat type selection page
            else:
                return render(request, 'login.html', {'not_active': True})  # Account not active
        else:
            return render(request, 'login.html', {'not_found': True})  # Account not found

    # Render the login page if it's a GET request
    else:
        return render(request, 'login.html')

    
# Log out
def logout(request):
    if 'email' in request.session.keys():
        del request.session['email']
        return redirect('index')
    else:
        return redirect('index')


def CreateRoom(request):

    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']

        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=username)

        except Room.DoesNotExist:
            new_room = Room(room_name = room)
            new_room.save()
            return redirect('room', room_name=room, username=username)

    return render(request, 'Room.html')
    



def MessageView(request, room_name, username):

    get_room = Room.objects.get(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']

        print(message)

        new_message = Message(room=get_room, sender=username, message=message)
        new_message.save()

    get_messages= Message.objects.filter(room=get_room)
    
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    }
    return render(request, 'message.html', context)

def chatPage(request, username=None):
    if request.method == 'POST':
        chat_type = request.POST.get('chat_type')
        if chat_type == 'personal':
            return redirect('private_chat')
        elif chat_type == 'group':
            return redirect('create-room')
        else: 
            return redirect('index')

    if username:
        user_obj = User.objects.get(username=username)
    else:
        user_obj = None

    users = User.objects.exclude(username=request.user.username)
    return render(request, 'chat_type.html', context={'user': user_obj, 'users': users})
 
# privatechat 
def Private_chat(request):
    frnd_name = request.GET.get('user',None)
    mychats_data = None
    if frnd_name:
        if User.objects.filter(username=frnd_name).exists() and PrivateChat.objects.filter(me=request.user,frnd=User.objects.get(username=frnd_name)).exists():
            frnd_ = User.objects.get(username=frnd_name)
            mychats_data = PrivateChat.objects.get(me=request.user,frnd=frnd_).chats
    frnds = User.objects.exclude(pk=request.user.id)
    return render(request,'privatechat.html',{'my':mychats_data,'chats': mychats_data,'frnds':frnds})

