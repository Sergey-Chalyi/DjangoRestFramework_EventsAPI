from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from events.models import Event
from events.serializers import EventSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


class EventsAPIViews(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]




class EventDetailAPIViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


def login(request):
    return render(request, 'login.html')


@login_required
def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('login')
