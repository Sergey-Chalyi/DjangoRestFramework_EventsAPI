from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from events.models import Event
from events.serializers import EventSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить GET, HEAD или OPTIONS запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешить изменения только если пользователь является организатором
        return obj.organizer == request.user



class EventsAPIViews(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventDetailAPIViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]



def login(request):
    return render(request, 'login.html')


@login_required
def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('login')
