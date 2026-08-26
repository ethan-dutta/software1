from re import A
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Message
from .serializer import MessageSerializer
from rest_framework.views import APIView
from django.shortcuts import render
import requests

def index(request):
    if request.method == "GET":  
        home_team = request.GET.get("home_team")
        print(f"Home Team: {home_team}")
        for event_id in event_ids:
            api_call = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/lookupevent.php?id={event_id}")
            if api_call is not None:
                storage = api_call.json()
            for event in storage["events"]:
                date_event = event["dateEvent"]
                home_team = event["strHomeTeam"]
                away_team = event["strAwayTeam"]
                home_score = event["intHomeScore"]
                away_score = event["intAwayScore"]

            print(f"{date_event}: {home_team} vs {away_team}")
    return render(request, "myapp/index.html")



event_ids = [2052711, 2052712, 2052713, 2052714]

# index(event_ids)


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def delete(self, request, *args, **kwargs):
        # Delete all messages
        self.queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'id'

class MessagePostList(APIView):
    def get(self, request, format=None):
        title = request.query_params.get('title', "")
        if title:
            messages = Message.objects.filter(title__icontains=title)
        else:
            messages = Message.objects.all()

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)