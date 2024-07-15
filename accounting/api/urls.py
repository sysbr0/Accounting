# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.message_list, name='message-list'),
    path('messages/<int:pk>/', views.message_detail, name='message-detail'),
]
