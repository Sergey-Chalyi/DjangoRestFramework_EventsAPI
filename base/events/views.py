from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from events.models import Event
from events.serializers import EventSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


class EventsAPIViews(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer



class EventDetailAPIViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

