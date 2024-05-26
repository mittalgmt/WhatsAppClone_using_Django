
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),  # Index page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('login/', views.login_view, name='login'),  
    path('logout/',views.logout,name="logout"),# Login page
    path('chat-type/', views.chatPage, name='chat_type'),  # Chat type selection page
    path('private-chat', views.Private_chat, name='private_chat'),
    path('create-room/', views.CreateRoom, name='create-room'),  # Create room page
    path('<str:room_name>/<str:username>/', views.MessageView, name='room'),  # Room page
]