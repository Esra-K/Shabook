from . import views
from .views import (BookListView, UserBookListView, BookCreateView, 
                    BookUpdateView, BookDeleteView, BookDetailView,
                    MessageCreateView, MessageDeleteView, InboxMessageListView,
                     OutboxMessageListView, MessageDetailView, MessageReplyView,SearchView)
from django.urls import path

from django.conf.urls import url

urlpatterns = [
    path('message/reply/<str:username>/forpost/<int:post>/', MessageReplyView.as_view(), name='message-reply'),

    path('home', views.home , name = 'shabook-home'),
    path('h1', BookListView.as_view(), name='shabook-home1'),
    path('user/<str:username>', UserBookListView.as_view(), name='user-posts'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='post-detail'),
    path('book/new/', BookCreateView.as_view(), name='post-create'),
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name='post-update'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='post-delete'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('in/<str:username>/', InboxMessageListView.as_view(), name='in-box'),
    path('out/<str:username>/', OutboxMessageListView.as_view(), name='out-box'),
    path('message/new/<int:post>/', MessageCreateView.as_view(), name='message-create'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message-delete'),
    url('search', SearchView.as_view(), name='query'),

]


