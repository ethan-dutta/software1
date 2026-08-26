from django.urls import path
from rest_framework import urlpatterns
from . import views

urlpatterns = [
    path("messages/", views.MessageListCreateView.as_view(), name="message-list-create"),
    path(
        "messages/<int:id>/", 
         views.MessageRetrieveUpdateDestroyView.as_view(), 
         name="update",
    ),

]


