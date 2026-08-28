from multiprocessing import context
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
    context = {}
    money = 1000
    context["money"] = money
    if request.method == "GET":  
        teamoo = request.GET.get("textfield")
        print(f"Teamoo: {teamoo}")
        if teamoo:
            api_call = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/searchteams.php?t={teamoo}")
            if api_call.status_code == 200:
                storage = api_call.json()
                home_id = storage["teams"][0]["idTeam"]
                api_specific = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/eventslast.php?id={home_id}")
                data = api_specific.json()
                print(data)

                for result in data["results"]:
                    home_team= result["strHomeTeam"]
                    away_team = result["strAwayTeam"]
                    home_score = result["intHomeScore"]
                    away_score = result["intAwayScore"]
                    context["home_score"] = home_score
                    context["away_score"] = away_score
                    context["home_team"] = home_team
                    context["away_team"] = away_team
    return render(request, "myapp/index.html", context)


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